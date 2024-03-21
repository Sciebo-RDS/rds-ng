import typing

from common.py.core.logging import debug
from common.py.core.messaging import Channel
from common.py.utils import UnitID

from gate.data.storage.session import SessionStorage

SERVER_CHANNEL_KEY = "server_channel"


def set_server_channel(server_id: UnitID) -> None:
    """
    Sets the global server channel.

    Args:
        server_id: The server ID.
    """
    SessionStorage.set_data(
        SessionStorage.GLOBAL_SESSION, SERVER_CHANNEL_KEY, Channel.direct(server_id)
    )

    debug("Assigned server channel", scope="network", target=server_channel())


def reset_server_channel() -> None:
    """
    Resets the global server channel.
    """
    SessionStorage.clear_data(SessionStorage.GLOBAL_SESSION, SERVER_CHANNEL_KEY)

    debug("Reset server channel", scope="network")


def has_server_channel() -> bool:
    """
    Checks whether a global server channel is available.
    """
    return SessionStorage.has_data(SessionStorage.GLOBAL_SESSION, SERVER_CHANNEL_KEY)


def server_channel() -> Channel:
    """
    Retrieves the global server channel.

    Returns:
        The global server channel, if any.

    Raises:
        RuntimeError: If no server channel has been set.
    """
    if not has_server_channel():
        raise RuntimeError("Tried to access a non-existing server channel")

    return typing.cast(
        Channel,
        SessionStorage.get_data(SessionStorage.GLOBAL_SESSION, SERVER_CHANNEL_KEY),
    )
