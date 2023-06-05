from dataclasses import dataclass

from .message import Message


@dataclass(frozen=True, kw_only=True)
class CommandReply(Message):
    success: bool = True
    message: str = ""
