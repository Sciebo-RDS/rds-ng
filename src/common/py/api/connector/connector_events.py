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
from ...data.entities.authorization import AuthorizationSettings
from ...data.entities.connector import (
    Connector,
    ConnectorID,
    ConnectorCategoryID,
    ConnectorMetadataProfile,
)


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


@Message.define("event/connector/announce")
class ConnectorAnnounceEvent(Event):
    """
    Emitted by a connector to let the server know about its existence.
    """

    connector_id: ConnectorID

    display_name: str
    description: str
    category: ConnectorCategoryID

    authorization: AuthorizationSettings = dataclasses.field(
        default_factory=AuthorizationSettings
    )
    options: Connector.Options = Connector.Options.DEFAULT

    logos: Connector.Logos = dataclasses.field(default_factory=Connector.Logos)

    metadata_profile: ConnectorMetadataProfile = dataclasses.field(default_factory=dict)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        connector_id: ConnectorID,
        name: str,
        description: str,
        category: ConnectorCategoryID,
        authorization: AuthorizationSettings,
        options: Connector.Options,
        logos: Connector.Logos,
        metadata_profile: ConnectorMetadataProfile,
        chain: Message | None = None
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(
            ConnectorAnnounceEvent,
            chain,
            connector_id=connector_id,
            display_name=name,
            description=description,
            category=category,
            authorization=authorization,
            options=options,
            logos=logos,
            metadata_profile=metadata_profile,
        )
