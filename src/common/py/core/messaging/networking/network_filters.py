import typing

from .network_filter import NetworkFilter
from .. import Message
from ..meta import MessageMetaInformation


class NetworkFilters:
    """
    A list of network filters.
    """

    def __init__(self):
        self._filters: typing.List[NetworkFilter] = []

    def install(self, fltr: NetworkFilter) -> None:
        """
        Adds a new filter.

        Args:
            fltr: The filter to add.
        """
        if fltr not in self._filters:
            self._filters.append(fltr)

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
        return any(f.filter_incoming_message(msg, msg_meta) for f in self._filters)

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
            Whether the message should pass.
        """
        return any(
            f.filter_outgoing_message(msg, msg_meta, connection) for f in self._filters
        )
