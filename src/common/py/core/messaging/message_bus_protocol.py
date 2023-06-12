from typing import Protocol

from .message import Message


class MessageBusProtocol(Protocol):
    def dispatch(self, msg: Message) -> None: ...
