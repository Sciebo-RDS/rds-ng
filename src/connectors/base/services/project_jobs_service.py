from common.py.component import BackendComponent
from common.py.services import Service


def create_project_jobs_service(comp: BackendComponent) -> Service:
    """
    Creates the project jobs service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    from common.py.api.project import StartProjectJobCommand, StartProjectJobReply

    from .connector_service_context import ConnectorServiceContext

    svc = comp.create_service(
        "Project jobs service", context_type=ConnectorServiceContext
    )

    @svc.message_handler(StartProjectJobCommand)
    def start_job(msg: StartProjectJobCommand, ctx: ConnectorServiceContext) -> None:
        # TODO: Actually do something with the job
        StartProjectJobReply.build(
            ctx.message_builder,
            msg,
            project_id=msg.project.project_id,
            connector_instance=msg.connector_instance,
        ).emit()

    return svc
