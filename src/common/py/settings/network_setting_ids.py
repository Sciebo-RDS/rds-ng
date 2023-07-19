from ..utils.config import SettingID


class NetworkServerSettingIDs:
    """
    Identifiers for server-specific networking settings.

    Attributes:
        ALLOWED_ORIGINS: A comma-separated list of allowed origins; use the asterisk (*) to allow all (value type: ``string``).
    """
    ALLOWED_ORIGINS = SettingID("network.server", "allowed_origins")


class NetworkClientSettingIDs:
    """
    Identifiers for client-specific networking settings.

    Attributes:
        SERVER_ADDRESS: The address of the server the client should automatically connect to (value type: ``string``).
        CONNECTION_TIMEOUT: The maximum time (in seconds) for connection attempts (value type: ``float``).
    """
    SERVER_ADDRESS = SettingID("network.client", "server_address")
    CONNECTION_TIMEOUT = SettingID("network.client", "connection_timeout")
