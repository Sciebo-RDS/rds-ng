import typing
from typing import Protocol

from .message import Message
from .meta import MessageMetaInformationType


class MessageBusProtocol(Protocol):
    def dispatch(self, msg: Message, msg_meta: typing.Generic[MessageMetaInformationType]) -> None: ...
