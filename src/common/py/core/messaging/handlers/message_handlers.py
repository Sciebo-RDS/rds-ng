import threading
import typing
from pathlib import PurePosixPath

from ..message import MessageName, Message, MessageType
from .message_handler import MessageHandler, MessageHandlerMapping, MessageHandlerMappings


class MessageHandlers:
    """
    Holds mappings for message handlers.
    """
    def __init__(self):
        self._handlers: MessageHandlerMappings = []
        
        self._lock = threading.Lock()
        
    def add_handler(self, fltr: str, handler: MessageHandler, message_type: type[MessageType] = Message, is_async: bool = False) -> None:
        """
        Adds a new message handler mapping.
        
        Args:
            fltr: The message name filter.
            handler: The message handler.
            message_type: The message type the handler expects.
            is_async: Whether the handler should be invoked asynchronously in its own thread.
        """
        with self._lock:
            self._handlers.append(MessageHandlerMapping(fltr, handler, message_type, is_async))
            
    def find_handlers(self, msg_name: MessageName) -> MessageHandlerMappings:
        """
        Finds all handlers that fit the given `msg_name`.
        
        The message name filter can be a complete message name, or a wildcard pattern using asterisks (`*`).
        
        Args:
            msg_name: The message name (pattern).

        Returns:
            A list of all found message handlers.
        """
        handlers: MessageHandlerMappings = []
        with self._lock:
            for mapping in self._handlers:
                if PurePosixPath(msg_name).match(mapping.filter):
                    handlers.append(mapping)
        return handlers

    def __str__(self) -> str:
        return "; ".join(map(str, self._handlers))
