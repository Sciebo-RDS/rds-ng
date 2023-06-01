from .message_dispatcher import MessageDispatcher
from ..event import Event


class EventDispatcher(MessageDispatcher[Event]):
    def __init__(self):
        super().__init__()
        
    def dispatch(self, event: Event):
        raise RuntimeError("Too lazy for event stuff")
