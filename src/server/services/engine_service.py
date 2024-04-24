from common.py.component import BackendComponent
from common.py.services import Service


def create_engine_service(comp: BackendComponent) -> Service:
    """
    Creates the server engine service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """
    from common.py.api.component import ComponentProcessEvent

    from .server_service_context import ServerServiceContext

    svc = comp.create_service("Engine service", context_type=ServerServiceContext)

    @svc.message_handler(ComponentProcessEvent)
    def process_engine(msg: ComponentProcessEvent, ctx: ServerServiceContext) -> None:
        ctx.engine.process()

    return svc
