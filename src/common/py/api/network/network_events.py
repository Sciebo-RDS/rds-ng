import dataclasses

from ...core.messaging import Event, Message
from ...core.messaging.composers import MessageBuilder, EventComposer
from ...utils import UnitID


@Message.define("event/network/client-connected")
class ClientConnectedEvent(Event):
    """
    Emitted whenever the ``Client`` established a connection to the server.
    """

    @staticmethod
    def build(
        message_builder: MessageBuilder, *, chain: Message | None = None
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(ClientConnectedEvent, chain)


@Message.define("event/network/client-disconnected")
class ClientDisconnectedEvent(Event):
    """
    Emitted whenever the ``Client`` cuts its connection from the server.
    """

    @staticmethod
    def build(
        message_builder: MessageBuilder, *, chain: Message | None = None
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(ClientDisconnectedEvent, chain)


@Message.define("event/network/client-connection-error")
class ClientConnectionErrorEvent(Event):
    """
    Emitted whenever the ``Client`` is unable to establish a connection.

    Attributes:
        reason: The connection error reason.
    """

    reason: str = ""

    @staticmethod
    def build(
        message_builder: MessageBuilder, *, reason: str, chain: Message | None = None
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(
            ClientConnectionErrorEvent, chain, reason=reason
        )


@Message.define("event/network/server-connected")
class ServerConnectedEvent(Event):
    """
    Emitted whenever the ``Server`` established a connection to a client.

    Attributes:
        client_id: The internal client ID.
    """

    comp_id: UnitID = dataclasses.field(default_factory=lambda: UnitID("", ""))
    client_id: str = ""

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        comp_id: UnitID,
        client_id: str,
        chain: Message | None = None
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(
            ServerConnectedEvent, chain, comp_id=comp_id, client_id=client_id
        )


@Message.define("event/network/server-disconnected")
class ServerDisconnectedEvent(Event):
    """
    Emitted whenever the ``Server`` cuts a connection from a client.

    Attributes:
        client_id: The internal client ID.
    """

    comp_id: UnitID = dataclasses.field(default_factory=lambda: UnitID("", ""))
    client_id: str = ""

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        comp_id: UnitID,
        client_id: str,
        chain: Message | None = None
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(
            ServerConnectedEvent, chain, comp_id=comp_id, client_id=client_id
        )
