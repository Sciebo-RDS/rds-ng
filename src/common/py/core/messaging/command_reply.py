import typing
import uuid
from dataclasses import dataclass, field
from enum import IntEnum, auto

from .message import Message, Trace


@dataclass(frozen=True, kw_only=True)
class CommandReply(Message):
    class FailType(IntEnum):
        NONE = 0
        TIMEOUT = auto()
        EXCEPTION = auto()
        UNKNOWN = auto()
    
    success: bool = True
    message: str = ""
    
    unique: Trace = field(default_factory=uuid.uuid4)


CommandReplyType = typing.TypeVar("CommandReplyType", bound=CommandReply)

CommandDoneCallback = typing.Callable[[CommandReplyType, bool, str], None]
CommandFailCallback = typing.Callable[[CommandReply.FailType, str], None]
