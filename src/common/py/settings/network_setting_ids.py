from ..utils.config import SettingID


class NetworkServerSettingIDs:
    ALLOWED_ORIGINS = SettingID("network.server", "allowed_clients")


class NetworkClientSettingIDs:
    SERVER_ADDRESS = SettingID("network.client", "server_address")
