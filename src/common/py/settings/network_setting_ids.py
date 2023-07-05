from ..utils.config import SettingID


class NetworkServerSettingIDs:
    ALLOWED_ORIGINS = SettingID("network.server", "allowed_origins")


class NetworkClientSettingIDs:
    SERVER_ADDRESS = SettingID("network.client", "server_address")
    CONNECTION_TIMEOUT = SettingID("network.client", "connection_timeout")
