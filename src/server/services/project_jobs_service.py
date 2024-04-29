from common.py.component import BackendComponent
from common.py.core.messaging import Channel
from common.py.data.entities.project import ProjectJob
from common.py.services import Service

from .tools.project_job_tools import send_project_jobs_list


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
        if (
            job := ctx.storage_pool.project_job_storage.get(
                (msg.project_id, msg.connector_instance)
            )
        ) is not None:
            job.message = "Job started"

            if (
                session := ctx.session_manager.find_user_session(job.user_id)
            ) is not None:
                send_project_jobs_list(msg, ctx, session=session)

    @svc.message_handler(ComponentProcessEvent)
    def process_jobs(msg: ComponentProcessEvent, ctx: ServerServiceContext) -> None:
        pass

    return svc
