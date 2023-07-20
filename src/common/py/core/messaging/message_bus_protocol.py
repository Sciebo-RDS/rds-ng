from typing import Protocol

from .message import Message
from .meta import MessageMetaInformationType


class MessageBusProtocol(Protocol):
    """
    Defines the general interface for the ``MessageBus``.
    """
    def dispatch(self, msg: Message, msg_meta: MessageMetaInformationType) -> None: ...
