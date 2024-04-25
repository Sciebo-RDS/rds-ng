import time

from common.py.component import BackendComponent
from common.py.data.entities.project import ProjectJob
from common.py.services import Service


def create_jobs_service(comp: BackendComponent) -> Service:
    """
    Creates the jobs service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """
    from common.py.api.project import InitiateJobCommand, InitiateJobReply
    from common.py.api.component import ComponentProcessEvent

    from .server_service_context import ServerServiceContext

    svc = comp.create_service("Jobs service", context_type=ServerServiceContext)

    @svc.message_handler(InitiateJobCommand)
    def initiate_job(msg: InitiateJobCommand, ctx: ServerServiceContext) -> None:
        if not ctx.ensure_user(msg, InitiateJobReply):
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
                project_id=msg.project_id,
                connector_instance=msg.connector_instance,
                message="Job started",
            )

            ctx.storage_pool.project_job_storage.add(job)
            success = True
        else:
            message = "A job through this connection is already running"

        # TODO: Logging

        InitiateJobReply.build(
            ctx.message_builder, msg, success=success, message=message
        ).emit()

    @svc.message_handler(ComponentProcessEvent)
    def process_jobs(msg: ComponentProcessEvent, ctx: ServerServiceContext) -> None:
        pass

    return svc
