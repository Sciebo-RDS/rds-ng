from ..core.messaging import Event, Message


@Message.define("event/network/client-connected")
class ClientConnectedEvent(Event):
    """
    Emitted whenever the ``Client`` established a connection to the server.
    """


@Message.define("event/network/client-disconnected")
class ClientDisconnectedEvent(Event):
    """
    Emitted whenever the ``Client`` cuts its connection from the server.
    """


@Message.define("event/network/client-connection-error")
class ClientConnectionErrorEvent(Event):
    """
    Emitted whenever the ``Client`` is unable to establish a connection.
    """

    reason: str = ""


@Message.define("event/network/server-connected")
class ServerConnectedEvent(Event):
    """
    Emitted whenever the ``Server`` established a connection to a client.
    """

    client_id: str = ""


@Message.define("event/network/server-disconnected")
class ServerDisconnectedEvent(Event):
    """
    Emitted whenever the ``Server`` cuts a connection from a client.
    """

    client_id: str = ""
