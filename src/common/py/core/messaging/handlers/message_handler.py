import typing
from dataclasses import dataclass

from ..message import MessageType
from .message_context import MessageContextType

MessageHandler = typing.Callable[[MessageType, MessageContextType], None]


@dataclass(frozen=True)
class MessageHandlerMapping:
    """
    Mapping from a message name filter to a message handler.
    
    Attributes:
        filter: The message name filter.
        handler: The message handler.
        message_type: The message type the handler expects.
        is_async: Whether the handler should be invoked asynchronously in its own thread.
    """
    filter: str
    handler: MessageHandler
    message_type: type[MessageType]
    is_async: bool = False
    
    def __str__(self) -> str:
        return f"{self.filter} -> {str(self.handler)} [{str(self.message_type)}]"


MessageHandlerMappings = typing.List[MessageHandlerMapping]
