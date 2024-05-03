from common.py.component import BackendComponent
from common.py.core.logging import debug
from common.py.core.messaging import Channel
from common.py.data.entities.project import ProjectJob
from common.py.services import Service

from .tools import send_project_jobs_list, handle_project_job_message
from ..networking.session import Session


def create_project_jobs_service(comp: BackendComponent) -> Service:
    """
    Creates the jobs service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """
    from common.py.api.project import (
        ListProjectJobsCommand,
        ListProjectJobsReply,
        InitiateProjectJobCommand,
        InitiateProjectJobReply,
        StartProjectJobCommand,
        StartProjectJobReply,
        ProjectJobProgressEvent,
        ProjectJobCompletionEvent,
    )
    from common.py.api.component import ComponentProcessEvent

    from .server_service_context import ServerServiceContext

    svc = comp.create_service("Project jobs service", context_type=ServerServiceContext)

    @svc.message_handler(ListProjectJobsCommand)
    def list_jobs(msg: ListProjectJobsCommand, ctx: ServerServiceContext) -> None:
        if not ctx.ensure_user(msg, ListProjectJobsReply, jobs=[]):
            return

        ListProjectJobsReply.build(
            ctx.message_builder,
            msg,
            jobs=ctx.storage_pool.project_job_storage.filter_by_user(ctx.user.user_id),
        ).emit()

    @svc.message_handler(InitiateProjectJobCommand)
    def initiate_job(msg: InitiateProjectJobCommand, ctx: ServerServiceContext) -> None:
        if not ctx.ensure_user(msg, InitiateProjectJobReply):
            return

        def _initiate(
            success: bool, message: str, job: ProjectJob | None = None
        ) -> None:
            if success and job is not None:
                ctx.storage_pool.project_job_storage.add(job)

            InitiateProjectJobReply.build(
                ctx.message_builder, msg, success=success, message=message
            ).emit()

            send_project_jobs_list(msg, ctx)

        from common.py.data.entities.connector import find_connector_by_instance_id
        from common.py.data.entities.project import find_project_by_id

        # Allow only one job per project & connection
        if (
            ctx.storage_pool.project_job_storage.get(
                (msg.project_id, msg.connector_instance)
            )
            is not None
        ):
            _initiate(False, "A job through this connection is already running")
            return

        # We need to find the proper project and connector first
        if (
            project := find_project_by_id(
                ctx.storage_pool.project_storage.filter_by_user(ctx.user.user_id),
                msg.project_id,
            )
        ) is None:
            _initiate(
                False,
                f"Project {msg.project_id} does not belong to the current user or could not be found",
            )
            return

        if (
            connector := find_connector_by_instance_id(
                ctx.storage_pool.connector_storage.list(),
                ctx.user.user_settings.connector_instances,
                msg.connector_instance,
            )
        ) is None:
            _initiate(
                False,
                f"The connector for instance {msg.connector_instance} could not be resolved",
            )
            return

        # Ensure that the connector instance is enabled in the project options
        if (
            not project.options.use_all_connector_instances
            and msg.connector_instance not in project.options.active_connector_instances
        ):
            _initiate(
                False,
                f"The connector instance {msg.connector_instance} is not enabled for the project",
            )
            return

        # All checks have passed, so initiate the job and send it to the connector
        job = ProjectJob(
            user_id=ctx.user.user_id,
            project_id=msg.project_id,
            connector_instance=msg.connector_instance,
            message="Job initiated",
        )

        _initiate(True, "", job)

        StartProjectJobCommand.build(
            ctx.message_builder,
            project=project,
            connector_instance=msg.connector_instance,
            chain=msg,
        ).emit(Channel.direct(connector.connector_address))

    @svc.message_handler(StartProjectJobReply)
    def job_started(msg: StartProjectJobReply, ctx: ServerServiceContext) -> None:
        def update_job(job: ProjectJob, _: Session) -> None:
            job.progress = 0.0
            job.message = "Job started"

            debug(
                "Job started",
                scope="jobs",
                user_id=job.user_id,
                project_id=job.project_id,
                connector_instance=job.connector_instance,
            )

        handle_project_job_message(
            (msg.project_id, msg.connector_instance), update_job, msg, ctx
        )

    @svc.message_handler(ProjectJobProgressEvent)
    def job_progress(msg: ProjectJobProgressEvent, ctx: ServerServiceContext) -> None:
        def update_job(job: ProjectJob, _: Session) -> None:
            job.progress = msg.progress
            job.message = msg.message

        handle_project_job_message(
            (msg.project_id, msg.connector_instance), update_job, msg, ctx
        )

    @svc.message_handler(ProjectJobCompletionEvent)
    def job_completion(
        msg: ProjectJobCompletionEvent, ctx: ServerServiceContext
    ) -> None:
        def update_job(job: ProjectJob, session: Session | None) -> None:
            if (
                project := ctx.storage_pool.project_storage.get(job.project_id)
            ) is not None:
                from common.py.data.entities.project.logbook import (
                    ProjectJobHistoryRecord,
                )

                record = ProjectJobHistoryRecord(
                    connector_instance=job.connector_instance,
                    success=msg.success,
                    message=msg.message,
                )

                project.logbook.job_history.append(record)

                if session:
                    from .tools.project_tools import send_projects_list

                    send_projects_list(msg, ctx, session=session)

            ctx.storage_pool.project_job_storage.remove(job)

            debug(
                "Job completed",
                scope="jobs",
                user_id=job.user_id,
                project_id=job.project_id,
                connector_instance=job.connector_instance,
                success=msg.success,
                message=msg.message,
            )

        handle_project_job_message(
            (msg.project_id, msg.connector_instance),
            update_job,
            msg,
            ctx,
        )

    @svc.message_handler(ComponentProcessEvent)
    def process_jobs(msg: ComponentProcessEvent, ctx: ServerServiceContext) -> None:
        pass

    return svc
