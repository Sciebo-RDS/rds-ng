from typing import Protocol

from .message import Message
from .meta import MessageMetaInformationType


class MessageBusProtocol(Protocol):
    # pylint: disable=missing-function-docstring,too-few-public-methods
    """
    Defines the general interface for the ``MessageBus``.
    """
    def dispatch(self, msg: Message, msg_meta: MessageMetaInformationType) -> None: ...
