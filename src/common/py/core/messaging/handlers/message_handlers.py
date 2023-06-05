import threading
import typing

from ..message import MessageName, Message, MessageType
from .message_handler import MessageHandler, MessageHandlerMapping, MessageHandlerMappings


class MessageHandlers:
    """ Holds mappings for message handlers. """
    def __init__(self):
        self._handlers: MessageHandlerMappings = []
        
        self._lock = threading.Lock()
        
    def add_handler(self, fltr: str, handler: MessageHandler, message_type: typing.Type[MessageType] = Message, is_async: bool = False) -> None:
        with self._lock:
            self._handlers.append(MessageHandlerMapping(fltr, handler, message_type, is_async))
            
    def find_handlers(self, msg_name: MessageName) -> MessageHandlerMappings:
        handlers: MessageHandlerMappings = []
        with self._lock:
            for mapping in self._handlers:
                if msg_name.match(mapping.filter):
                    handlers.append(mapping)
        return handlers

    def __str__(self) -> str:
        return "; ".join(map(str, self._handlers))
