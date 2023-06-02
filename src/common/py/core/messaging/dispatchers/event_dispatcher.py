from .message_dispatcher import MessageDispatcher
from ..event import Event
from ..handlers import MessageHandlersList


class EventDispatcher(MessageDispatcher[Event]):
    def __init__(self):
        super().__init__()
        
    def dispatch(self, event: Event, handlers: MessageHandlersList):
        for handler in handlers:
            handler[0](event)
