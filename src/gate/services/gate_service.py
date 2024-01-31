from common.py.api.network import ServerTimeoutEvent
from common.py.component import BackendComponent
from common.py.services import Service

from .gate_service_context import GateServiceContext


def create_gate_service(comp: BackendComponent) -> Service:
    """
    Creates the main gate service that reacts to general (mostly networking-related) messages.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.

    """

    svc = comp.create_service("Gate service")

    @svc.message_handler(ServerTimeoutEvent)
    def server_timeout(msg: ServerTimeoutEvent, ctx: GateServiceContext) -> None:
        ctx.logger.debug("A client timed out", scope="gate", client=msg.comp_id)

    return svc
