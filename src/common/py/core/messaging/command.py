import typing
from dataclasses import dataclass

from .message import Message


@dataclass(frozen=True, kw_only=True)
class Command(Message):
    pass


CommandType = typing.TypeVar("CommandType", bound=Command)
