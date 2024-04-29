from common.py.component import BackendComponent
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

        success = False
        message = ""

        if (
            ctx.storage_pool.project_job_storage.get(
                (msg.project_id, msg.connector_instance)
            )
            is None
        ):
            job = ProjectJob(
                user_id=ctx.user.user_id,
                project_id=msg.project_id,
                connector_instance=msg.connector_instance,
                message="Job started",
            )

            ctx.storage_pool.project_job_storage.add(job)
            success = True
        else:
            message = "A job through this connection is already running"

        InitiateProjectJobReply.build(
            ctx.message_builder, msg, success=success, message=message
        ).emit()

        send_project_jobs_list(msg, ctx)

    @svc.message_handler(ComponentProcessEvent)
    def process_jobs(msg: ComponentProcessEvent, ctx: ServerServiceContext) -> None:
        pass

    return svc
