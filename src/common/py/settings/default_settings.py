import typing

from .general_setting_ids import GeneralSettingIDs
from .component_setting_ids import ComponentSettingIDs
from .network_setting_ids import NetworkServerSettingIDs, NetworkClientSettingIDs
from ..utils.config import SettingID


def get_default_settings() -> typing.Dict[SettingID, typing.Any]:
    """
    Gets default values for all settings.
    
    Returns:
        A dictionary mapping the setting identifiers to their default values.
    """
    return {
        GeneralSettingIDs.DEBUG: False,
        
        ComponentSettingIDs.INSTANCE: "default",
        
        NetworkServerSettingIDs.ALLOWED_ORIGINS: "",
        
        NetworkClientSettingIDs.SERVER_ADDRESS: "",
        NetworkClientSettingIDs.CONNECTION_TIMEOUT: 10,
    }
