from dataclasses import dataclass

from . import Message


@dataclass(frozen=True, kw_only=True)
class Event(Message):
    pass
