import typing

from .message_dispatcher import MessageDispatcher
from ..event import Event
from ..handlers import MessageHandlerMapping
from ...service import ServiceContextType


class EventDispatcher(MessageDispatcher[Event]):
    def dispatch(self, event: Event, handler: MessageHandlerMapping, ctx: typing.Generic[ServiceContextType]) -> None:
        print("RECV EVENT")
        super().dispatch(event, handler, ctx)
