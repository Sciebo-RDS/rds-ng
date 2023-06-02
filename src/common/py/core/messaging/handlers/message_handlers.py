import threading
import typing
from dataclasses import dataclass

from ..message import Message, MessageType
from ..message_name import MessageName
from .message_handler import MessageHandler

MessageHandlersList = typing.List[typing.Tuple[MessageHandler, MessageType]]


class MessageHandlers:
    """ Holds a mapping for message handlers. """
    @dataclass(frozen=True)
    class _HandlerMapping:
        filter: str
        handler: MessageHandler
        message_type: MessageType
        
    def __init__(self):
        self._handlers: typing.List[MessageHandlers._HandlerMapping] = []
        
        self._lock = threading.Lock()
        
    def add_handler(self, fltr: str, handler: MessageHandler, message_type: MessageType = Message) -> None:
        with self._lock:
            self._handlers.append(MessageHandlers._HandlerMapping(fltr, handler, message_type))
            
    def find_handlers(self, msg_name: MessageName) -> MessageHandlersList:
        handlers: MessageHandlersList = []
        with self._lock:
            for mapping in self._handlers:
                if msg_name.match(mapping.filter):
                    handlers.append((mapping.handler, mapping.message_type))
        return handlers

    def __str__(self) -> str:
        return str(self._handlers)
