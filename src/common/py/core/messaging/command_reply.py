import typing
import uuid
from dataclasses import dataclass, field
from enum import IntEnum, auto

from .message import Message, Trace


@dataclass(frozen=True, kw_only=True)
class CommandReply(Message):
    """
    A command reply message.

    Every command needs to receive a reply in the form of a ``CommandReply`` message. The reply contains
    information about its ``success``, as well as a text message which is usually used to describe reasons for
    failures.

    Attributes:
        success: Whether the command succeeded.
        message: Arbitrary text, usually used to describe reasons for failures.
        unique: The unique identifier of its corresponding command.
    """
    class FailType(IntEnum):
        """
        Used when a command failed.
        """
        NONE = 0
        TIMEOUT = auto()
        EXCEPTION = auto()
        UNKNOWN = auto()
    
    success: bool = True
    message: str = ""
    
    unique: Trace = field(default_factory=uuid.uuid4)


CommandReplyType = typing.TypeVar("CommandReplyType", bound=CommandReply)  # pylint: disable=invalid-name

CommandDoneCallback = typing.Callable[[CommandReplyType, bool, str], None]
CommandFailCallback = typing.Callable[[CommandReply.FailType, str], None]
