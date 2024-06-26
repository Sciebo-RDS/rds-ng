from common.py.component import BackendComponent
from common.py.core.logging import debug, error
from common.py.core.messaging import Channel
from common.py.data.entities.authorization import get_host_authorization_token_id
from common.py.data.entities.project import ProjectJob
from common.py.data.entities.project.logbook import (
    append_logbook_record,
    ProjectJobHistoryRecord,
)
from common.py.services import Service

from .tools import (
    send_project_jobs_list,
    handle_project_job_message,
    send_project_logbook,
)
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

        # A broker token must be present, too
        if (broker_token := ctx.session.broker_token) is None:
            _initiate(
                False,
                f"No broker token has been assigned to the user",
            )
            return

        # Fetch the host authorization token; this can be *None* if the host doesn't require any authorization
        auth_token = ctx.storage_pool.authorization_token_storage.get(
            get_host_authorization_token_id(ctx.user)
        )

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
            user_token=ctx.session.user_token,
            auth_token=auth_token,
            broker_token=broker_token,
            chain=msg,
        ).emit(Channel.direct(connector.connector_address))

    @svc.message_handler(StartProjectJobReply)
    def job_started(msg: StartProjectJobReply, ctx: ServerServiceContext) -> None:
        project = ctx.storage_pool.project_storage.get(msg.project_id)

        def update_job(job: ProjectJob) -> None:
            if msg.success:
                job.progress = 0.0
                job.message = "Job started"

                debug(
                    "Job started",
                    scope="jobs",
                    user_id=job.user_id,
                    project_id=job.project_id,
                    connector_instance=job.connector_instance,
                )
            else:
                if project is not None:
                    append_logbook_record(
                        project.logbook.job_history,
                        ProjectJobHistoryRecord(
                            connector_instance=job.connector_instance,
                            success=False,
                            message=f"Job start failed: {msg.message}",
                        ),
                    )

                ctx.storage_pool.project_job_storage.remove(job)

                error(
                    "Job start failed",
                    scope="jobs",
                    user_id=job.user_id,
                    project_id=job.project_id,
                    connector_instance=job.connector_instance,
                    error=msg.message,
                )

        def notify_job(job: ProjectJob, session: Session) -> None:
            if project is not None:
                send_project_logbook(msg, ctx, project, session=session)

        handle_project_job_message(
            (msg.project_id, msg.connector_instance),
            msg,
            ctx,
            update_callback=update_job,
            notify_callback=notify_job,
        )

    @svc.message_handler(ProjectJobProgressEvent)
    def job_progress(msg: ProjectJobProgressEvent, ctx: ServerServiceContext) -> None:
        def update_job(job: ProjectJob) -> None:
            if ProjectJobProgressEvent.Contents.MESSAGE in msg.contents:
                job.progress = msg.progress

            if ProjectJobProgressEvent.Contents.PROGRESS in msg.contents:
                job.message = msg.message

        handle_project_job_message(
            (msg.project_id, msg.connector_instance),
            msg,
            ctx,
            update_callback=update_job,
        )

    @svc.message_handler(ProjectJobCompletionEvent)
    def job_completion(
        msg: ProjectJobCompletionEvent, ctx: ServerServiceContext
    ) -> None:
        project = ctx.storage_pool.project_storage.get(msg.project_id)

        def update_job(job: ProjectJob) -> None:
            if project is not None:
                append_logbook_record(
                    project.logbook.job_history,
                    ProjectJobHistoryRecord(
                        connector_instance=job.connector_instance,
                        success=msg.success,
                        message=msg.message,
                    ),
                )

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

        def notify_job(job: ProjectJob, session: Session) -> None:
            # Bounce the message off to the user to inform him about the completion
            ProjectJobCompletionEvent.build(
                ctx.message_builder,
                project_id=msg.project_id,
                connector_instance=msg.connector_instance,
                success=msg.success,
                message=msg.message,
                chain=msg,
            ).emit(Channel.direct(session.user_origin))

            # Send the updated project logbook to the client
            if project is not None:
                send_project_logbook(msg, ctx, project, session=session)

        handle_project_job_message(
            (msg.project_id, msg.connector_instance),
            msg,
            ctx,
            update_callback=update_job,
            notify_callback=notify_job,
        )

    return svc
