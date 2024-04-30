from common.py.component import BackendComponent
from common.py.core.logging import info
from common.py.services import Service

from ..data.entities.connector import ConnectorJob


def create_project_jobs_service(comp: BackendComponent) -> Service:
    """
    Creates the project jobs service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    from common.py.api.component import ComponentProcessEvent
    from common.py.api.project import StartProjectJobCommand, StartProjectJobReply

    from .connector_service_context import ConnectorServiceContext

    svc = comp.create_service(
        "Project jobs service", context_type=ConnectorServiceContext
    )

    @svc.message_handler(StartProjectJobCommand)
    def start_job(msg: StartProjectJobCommand, ctx: ConnectorServiceContext) -> None:
        info(
            "Starting new job",
            scope="jobs",
            project_id=msg.project.project_id,
            user_id=msg.project.user_id,
            connector_instance=msg.connector_instance,
        )

        job = ConnectorJob(
            project=msg.project, connector_instance=msg.connector_instance
        )
        ctx.jobs_engine.spawn(job, message_builder=ctx.message_builder)

        StartProjectJobReply.build(
            ctx.message_builder,
            msg,
            project_id=msg.project.project_id,
            connector_instance=msg.connector_instance,
        ).emit()

    @svc.message_handler(ComponentProcessEvent)
    def process_engine(
        msg: ComponentProcessEvent, ctx: ConnectorServiceContext
    ) -> None:
        ctx.jobs_engine.process()

    return svc
