import typing
from dataclasses import dataclass

from .message import Message
from .command import CommandType


@dataclass(frozen=True, kw_only=True)
class CommandReply(Message):
    success: bool = True
    message: str = ""
    
    command: CommandType | None = None


CommandReplyType = typing.TypeVar("CommandReplyType", bound=CommandReply)
CommandReplyCallback = typing.Callable[[CommandReplyType | None, ...], None]
