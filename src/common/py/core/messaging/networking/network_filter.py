from .. import Message
from ..meta import MessageMetaInformation


class NetworkFilter:
    """
    Filters incoming and outgoing network messages.
    """

    def filter_incoming_message(
        self, msg: Message, msg_meta: MessageMetaInformation
    ) -> bool:
        """
        Filters incoming messages.

        Args:
            msg: The incoming message.
            msg_meta: The message meta information.

        Returns:
            Whether the message should be filtered out.
        """
        return False

    def filter_outgoing_message(
        self,
        msg: Message,
        msg_meta: MessageMetaInformation,
        connection: MessageMetaInformation.Entrypoint,
    ) -> bool:
        """
        Filters outgoing messages.

        Args:
            msg: The outgoing message.
            msg_meta: The message meta information.
            connection: The connection type (server/client) over which the message is about to be sent.

        Returns:
            Whether the message should be filtered out.
        """
        return False
