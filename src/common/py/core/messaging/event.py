import typing
from dataclasses import dataclass

from .message import Message


@dataclass(frozen=True, kw_only=True)
class Event(Message):
    """
    An event message.

    Events are simple notifications that do not require a reply nor will *execute* anything.
    """
    pass


EventType = typing.TypeVar("EventType", bound=Event)
