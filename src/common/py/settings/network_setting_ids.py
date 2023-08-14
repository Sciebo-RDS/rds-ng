from ..utils.config import SettingID


class NetworkServerSettingIDs:
    # pylint: disable=too-few-public-methods
    """
    Identifiers for server-specific networking settings.

    Attributes:
        ALLOWED_ORIGINS: A comma-separated list of allowed origins; use the asterisk (*) to allow all (value type: ``string``).
        IDLE_TIMEOUT: The time (in seconds) until idle clients will be disconnected automatically; set to 0 to disable.
    """
    ALLOWED_ORIGINS = SettingID("network.server", "allowed_origins")
    IDLE_TIMEOUT = SettingID("network.server", "idle_timeout")


class NetworkClientSettingIDs:
    # pylint: disable=too-few-public-methods
    """
    Identifiers for client-specific networking settings.

    Attributes:
        SERVER_ADDRESS: The address of the server the client should automatically connect to (value type: ``string``).
        CONNECTION_TIMEOUT: The maximum time (in seconds) for connection attempts (value type: ``float``).
    """
    SERVER_ADDRESS = SettingID("network.client", "server_address")
    CONNECTION_TIMEOUT = SettingID("network.client", "connection_timeout")
