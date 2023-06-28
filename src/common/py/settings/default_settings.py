import typing

from .general_setting_ids import GeneralSettingIDs
from .component_setting_ids import ComponentSettingIDs
from .network_setting_ids import NetworkServerSettingIDs, NetworkClientSettingIDs
from ..utils.config import SettingID


def get_default_settings() -> typing.Dict[SettingID, typing.Any]:
    return {
        GeneralSettingIDs.DEBUG: False,
        
        ComponentSettingIDs.INSTANCE: "default",
        
        NetworkServerSettingIDs.ALLOWED_ORIGINS: "",
        
        NetworkClientSettingIDs.SERVER_ADDRESS: "",
    }
