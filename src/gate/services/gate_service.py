from common.py.api.network import (
    ServerTimeoutEvent,
    ClientConnectedEvent,
    ClientDisconnectedEvent,
    ClientConnectionErrorEvent,
)
from common.py.api.session import (
    GetSessionValueCommand,
    GetSessionValueReply,
    SetSessionValueCommand,
    SetSessionValueReply,
)
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

    svc = comp.create_service("Gate service", context_type=GateServiceContext)

    @svc.message_handler(ClientConnectedEvent)
    def client_connected(msg: ClientConnectedEvent, ctx: GateServiceContext) -> None:
        ctx.logger.debug("Server connection established", scope="gate")

    @svc.message_handler(ClientDisconnectedEvent)
    def client_disconnected(
        msg: ClientDisconnectedEvent, ctx: GateServiceContext
    ) -> None:
        ctx.logger.debug("Server connection terminated", scope="gate")

    @svc.message_handler(ClientConnectionErrorEvent)
    def client_connection_error(
        msg: ClientConnectionErrorEvent, ctx: GateServiceContext
    ) -> None:
        ctx.logger.debug(
            "Unable to establish a connection to the server",
            scope="gate",
            reason=msg.reason,
        )

    @svc.message_handler(ServerTimeoutEvent)
    def server_timeout(msg: ServerTimeoutEvent, ctx: GateServiceContext) -> None:
        ctx.logger.debug(
            "Clearing session data due to timeout", scope="gate", session=msg.comp_id
        )

        # A timeout automatically clears the session data of that client
        ctx.session_storage.clear_session(msg.comp_id)

    @svc.message_handler(GetSessionValueCommand)
    def get_session_value(msg: GetSessionValueCommand, ctx: GateServiceContext) -> None:
        ctx.logger.debug(
            "Retrieving session value", scope="gate", session=msg.origin, key=msg.key
        )

        value = ctx.session_storage.get_data(msg.origin, msg.key)
        GetSessionValueReply.build(ctx.message_builder, msg, value=value).emit()

    @svc.message_handler(SetSessionValueCommand)
    def set_session_value(msg: SetSessionValueCommand, ctx: GateServiceContext) -> None:
        ctx.logger.debug(
            "Setting session value",
            scope="gate",
            session=msg.origin,
            key=msg.key,
            value=msg.value,
        )

        ctx.session_storage.set_data(msg.origin, msg.key, msg.value)
        SetSessionValueReply.build(ctx.message_builder, msg).emit()

    return svc
