import typing
from dataclasses import dataclass

from .message import Message


@dataclass(frozen=True, kw_only=True)
class Event(Message):
    pass


EventType = typing.TypeVar("EventType", bound=Event)
