import typing
import uuid
from dataclasses import dataclass, field

from .message import Message, Trace


@dataclass(frozen=True, kw_only=True)
class Command(Message):
    unique: Trace = field(default_factory=uuid.uuid4)


CommandType = typing.TypeVar("CommandType", bound=Command)
