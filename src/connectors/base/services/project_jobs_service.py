from common.py.component import BackendComponent
from common.py.core.logging import info
from common.py.services import Service
from common.py.utils import EntryGuard

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
        success = False
        message = ""

        try:
            job = ConnectorJob(
                project=msg.project,
                connector_instance=msg.connector_instance,
                user_token=msg.user_token,
                broker_token=msg.broker_token,
            )
            ctx.jobs_engine.spawn(comp, svc, job, ctx)

            info(
                "Started new job",
                scope="jobs",
                project_id=msg.project.project_id,
                user_id=msg.project.user_id,
                connector_instance=msg.connector_instance,
            )

            success = True
        except Exception as exc:  # pylint: disable=broad-exception-caught
            message = f"Failed to start job: {str(exc)}"

        StartProjectJobReply.build(
            ctx.message_builder,
            msg,
            project_id=msg.project.project_id,
            connector_instance=msg.connector_instance,
            success=success,
            message=message,
        ).emit()

    @svc.message_handler(ComponentProcessEvent)
    def process_engine(
        msg: ComponentProcessEvent, ctx: ConnectorServiceContext
    ) -> None:
        with EntryGuard("process_engine") as guard:
            if not guard.can_execute:
                return

            ctx.jobs_engine.process()

    return svc
