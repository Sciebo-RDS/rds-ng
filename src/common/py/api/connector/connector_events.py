import dataclasses
import typing

from ...core.messaging import (
    Message,
    Event,
)
from ...core.messaging.composers import (
    MessageBuilder,
    EventComposer,
)
from ...data.entities import Connector


@Message.define("event/connector/list")
class ConnectorsListEvent(Event):
    """
    Emitted whenever the list of available connectors has been updated.

    Args:
        connectors: List of all connectors.
    """

    connectors: typing.List[Connector] = dataclasses.field(default_factory=list)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        connectors: typing.List[Connector],
        chain: Message | None = None
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(
            ConnectorsListEvent, chain, connectors=connectors
        )
