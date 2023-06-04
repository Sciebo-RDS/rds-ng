import typing
from dataclasses import dataclass

from ..message import MessageType

MessageHandler = typing.Callable[[MessageType], None]  # TODO: Subject to change (UoW, etc.)


@dataclass(frozen=True)
class MessageHandlerMapping:
    filter: str
    handler: MessageHandler
    message_type: MessageType
    
    def __str__(self) -> str:
        return f"{self.filter} -> {str(self.handler)} [{str(self.message_type)}]"


MessageHandlerMappings = typing.List[MessageHandlerMapping]
