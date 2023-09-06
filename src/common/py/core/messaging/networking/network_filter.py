from enum import IntEnum, auto

from .. import Message
from ..meta import MessageMetaInformation


class NetworkFilter:
    """
    Filters incoming and outgoing network messages.
    """

    class ConnectionType(IntEnum):
        """
        The affected connection type (client or server).
        """

        CLIENT = auto()
        SERVER = auto()

    def filter_incoming_message(
        self, connection: ConnectionType, msg: Message, msg_meta: MessageMetaInformation
    ) -> bool:
        """
        Filters incoming messages.

        Args:
            connection: The connection the message came through.
            msg: The incoming message.
            msg_meta: The message meta information.

        Returns:
            Whether the message should be filtered out.
        """
        return False

    def filter_outgoing_message(
        self, connection: ConnectionType, msg: Message, msg_meta: MessageMetaInformation
    ) -> bool:
        """
        Filters outgoing messages.

        Args:
            connection: The connection the message is sent through.
            msg: The outgoing message.
            msg_meta: The message meta information.

        Returns:
            Whether the message should be filtered out.
        """
        return False
