import typing
from dataclasses import dataclass

from ..message import MessageType

MessageHandler = typing.Callable[[MessageType, 'ServiceContextType'], None]  # We can't import anything from Service here due to cyclic dependencies


@dataclass(frozen=True)
class MessageHandlerMapping:
    filter: str
    handler: MessageHandler
    message_type: type[MessageType]
    is_async: bool = False
    
    def __str__(self) -> str:
        return f"{self.filter} -> {str(self.handler)} [{str(self.message_type)}]"


MessageHandlerMappings = typing.List[MessageHandlerMapping]
