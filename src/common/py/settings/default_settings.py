import typing

from ..utils.config import SettingID


def get_default_settings() -> typing.Dict[SettingID, typing.Any]:
    # pylint: disable=too-few-public-methods
    """
    Gets default values for all settings.

    Returns:
        A dictionary mapping the setting identifiers to their default values.
    """
    from .component_setting_ids import ComponentSettingIDs
    from .general_setting_ids import GeneralSettingIDs
    from .network_setting_ids import (
        NetworkSettingIDs,
        NetworkServerSettingIDs,
        NetworkClientSettingIDs,
    )

    return {
        # General settings
        GeneralSettingIDs.DEBUG: False,
        # Component settings
        ComponentSettingIDs.INSTANCE: "default",
        # Network settings
        NetworkSettingIDs.REGULAR_COMMAND_TIMEOUT: 10,
        NetworkSettingIDs.EXTERNAL_REQUESTS_TIMEOUT: 15,
        NetworkServerSettingIDs.ALLOWED_ORIGINS: "",
        NetworkServerSettingIDs.IDLE_TIMEOUT: 30 * 60,
        NetworkClientSettingIDs.SERVER_ADDRESS: "",
        NetworkClientSettingIDs.CONNECTION_TIMEOUT: 10,
    }
