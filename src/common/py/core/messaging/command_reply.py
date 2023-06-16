import typing
from dataclasses import dataclass
from enum import IntEnum, auto

from .message import Message
from .command import CommandType


@dataclass(frozen=True, kw_only=True)
class CommandReply(Message):
    class FailType(IntEnum):
        NONE = 0
        TIMEOUT = auto()
        EXCEPTION = auto()
        UNKNOWN = auto()
    
    success: bool = True
    message: str = ""
    
    command: CommandType | None = None


CommandReplyType = typing.TypeVar("CommandReplyType", bound=CommandReply)

CommandDoneCallback = typing.Callable[[CommandReplyType, bool, str], None]
CommandFailCallback = typing.Callable[[CommandReply.FailType, str], None]
