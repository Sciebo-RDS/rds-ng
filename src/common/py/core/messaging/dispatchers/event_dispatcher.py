from .message_dispatcher import MessageDispatcher
from ..event import Event
from ..handlers import MessageHandlerMapping
from ..meta import EventMetaInformation
from ...service import ServiceContextType


class EventDispatcher(MessageDispatcher[Event]):
    """
    Message dispatcher specific to ``Event``.
    """
    def __init__(self):
        super().__init__(EventMetaInformation)
    
    def dispatch(self, msg: Event, msg_meta: EventMetaInformation, handler: MessageHandlerMapping, ctx: ServiceContextType) -> None:
        """
        Dispatches a message to locally registered message handlers.

        Handlers can be either called synchronously or asynchronously, depending on how the handler was registered.

        Notes:
            Exceptions arising within a message handler will not interrupt the running program; instead, such errors will only be logged.

        Args:
            msg: The message to be dispatched.
            msg_meta: The message meta information.
            handler: The handler to be invoked.
            ctx: The service context.

        Raises:
            RuntimeError: If the handler requires a different message type.
        """
        ctx.logger.debug(f"Dispatching event: {msg}", scope="bus")
        super().dispatch(msg, msg_meta, handler, ctx)
