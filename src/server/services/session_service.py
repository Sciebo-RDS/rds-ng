from common.py.api.network import ServerTimeoutEvent
from common.py.api.session import (
    GetSessionValueCommand,
    GetSessionValueReply,
    SetSessionValueCommand,
    SetSessionValueReply,
)
from common.py.services import Service

from .server_service_context import ServerServiceContext
from ..component import ServerComponent


def create_session_service(comp: ServerComponent) -> Service:
    """
    Creates the session service that handles all session-related messages.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    svc = comp.create_service("Session service", context_type=ServerServiceContext)

    @svc.message_handler(ServerTimeoutEvent)
    def server_timeout(msg: ServerTimeoutEvent, ctx: ServerServiceContext) -> None:
        ctx.logger.debug(
            "Clearing session data due to timeout", scope="session", session=msg.comp_id
        )

        # A timeout automatically deletes the session for that client
        del ctx.session_manager[msg.comp_id]

    @svc.message_handler(GetSessionValueCommand)
    def get_session_value(
        msg: GetSessionValueCommand, ctx: ServerServiceContext
    ) -> None:
        ctx.logger.debug(
            "Retrieving session value", scope="session", session=msg.origin, key=msg.key
        )

        value = ctx.session_manager[msg.origin][msg.key]
        GetSessionValueReply.build(ctx.message_builder, msg, value=value).emit()

    @svc.message_handler(SetSessionValueCommand)
    def set_session_value(
        msg: SetSessionValueCommand, ctx: ServerServiceContext
    ) -> None:
        ctx.logger.debug(
            "Setting session value",
            scope="session",
            session=msg.origin,
            key=msg.key,
            value=msg.value,
        )

        ctx.session_manager[msg.origin][msg.key] = msg.value
        SetSessionValueReply.build(ctx.message_builder, msg).emit()

    return svc
