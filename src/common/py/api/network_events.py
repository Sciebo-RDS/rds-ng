import dataclasses

from ..core.messaging import Event, Message, Channel
from ..core.messaging.handlers import MessageEmitter
from ..utils import UnitID


@Message.define("event/network/client-connected")
class ClientConnectedEvent(Event):
    """
    Emitted whenever the ``Client`` established a connection to the server.
    """

    @staticmethod
    def emit(
        message_emitter: MessageEmitter,
        target: Channel,
        *,
        chain: Message | None = None
    ) -> None:
        """
        Helper function to easily emit this message.
        """
        message_emitter.emit_event(ClientConnectedEvent, target, chain=chain)


@Message.define("event/network/client-disconnected")
class ClientDisconnectedEvent(Event):
    """
    Emitted whenever the ``Client`` cuts its connection from the server.
    """

    @staticmethod
    def emit(
        message_emitter: MessageEmitter,
        target: Channel,
        *,
        chain: Message | None = None
    ) -> None:
        """
        Helper function to easily emit this message.
        """
        message_emitter.emit_event(ClientDisconnectedEvent, target, chain=chain)


@Message.define("event/network/client-connection-error")
class ClientConnectionErrorEvent(Event):
    """
    Emitted whenever the ``Client`` is unable to establish a connection.

    Attributes:
        reason: The connection error reason.
    """

    reason: str = ""

    @staticmethod
    def emit(
        message_emitter: MessageEmitter,
        target: Channel,
        *,
        reason: str,
        chain: Message | None = None
    ) -> None:
        """
        Helper function to easily emit this message.
        """
        message_emitter.emit_event(
            ClientConnectionErrorEvent, target, chain=chain, reason=reason
        )


@Message.define("event/network/server-connected")
class ServerConnectedEvent(Event):
    """
    Emitted whenever the ``Server`` established a connection to a client.

    Attributes:
        client_id: The internal client ID.
    """

    comp_id: UnitID = dataclasses.field(default_factory=UnitID)
    client_id: str = ""

    @staticmethod
    def emit(
        message_emitter: MessageEmitter,
        target: Channel,
        *,
        comp_id: UnitID,
        client_id: str,
        chain: Message | None = None
    ) -> None:
        """
        Helper function to easily emit this message.
        """
        message_emitter.emit_event(
            ServerConnectedEvent,
            target,
            chain=chain,
            comp_id=comp_id,
            client_id=client_id,
        )


@Message.define("event/network/server-disconnected")
class ServerDisconnectedEvent(Event):
    """
    Emitted whenever the ``Server`` cuts a connection from a client.

    Attributes:
        client_id: The internal client ID.
    """

    comp_id: UnitID = dataclasses.field(default_factory=UnitID)
    client_id: str = ""

    @staticmethod
    def emit(
        message_emitter: MessageEmitter,
        target: Channel,
        *,
        comp_id: UnitID,
        client_id: str,
        chain: Message | None = None
    ) -> None:
        """
        Helper function to easily emit this message.
        """
        message_emitter.emit_event(
            ServerDisconnectedEvent,
            target,
            chain=chain,
            comp_id=comp_id,
            client_id=client_id,
        )
