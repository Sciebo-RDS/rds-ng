import typing

from .message_dispatcher import MessageDispatcher
from ..event import Event
from ..handlers import MessageHandlerMapping
from ..meta import EventMetaInformation
from ...service import ServiceContextType


class EventDispatcher(MessageDispatcher[Event]):
    def __init__(self):
        super().__init__(EventMetaInformation)
    
    def dispatch(self, event: Event, event_meta: EventMetaInformation, handler: MessageHandlerMapping, ctx: ServiceContextType) -> None:
        ctx.logger.debug(f"Dispatching event: {event}", scope="bus")
        super().dispatch(event, event_meta, handler, ctx)
