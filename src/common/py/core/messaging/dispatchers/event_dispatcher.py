from .message_dispatcher import MessageDispatcher
from ..event import Event
from ..handlers import MessageHandlerMappings


class EventDispatcher(MessageDispatcher[Event]):
    def __init__(self):
        super().__init__()
        
    def dispatch(self, event: Event, handlers: MessageHandlerMappings):
        for handler in handlers:
            handler.handler(event)
