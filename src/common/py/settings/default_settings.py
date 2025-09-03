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
    from .integration_setting_ids import IntegrationSettingIDs
    from .network_setting_ids import (
        NetworkSettingIDs,
        NetworkServerSettingIDs,
        NetworkClientSettingIDs,
    )

    return {
        # General settings
        GeneralSettingIDs.DEBUG: False,
        GeneralSettingIDs.DEBUG_TRACE: False,
        # Component settings
        ComponentSettingIDs.INSTANCE: "default",
        # Network settings
        NetworkSettingIDs.API_KEY: "",
        NetworkSettingIDs.VERIFY_SSL: True,
        NetworkSettingIDs.TRANSMISSION_CHUNK_SIZE: 1 * 1024 * 1024,
        NetworkSettingIDs.REGULAR_COMMAND_TIMEOUT: 10,
        NetworkSettingIDs.EXTERNAL_REQUESTS_TIMEOUT: 60,
        NetworkServerSettingIDs.ALLOWED_ORIGINS: "",
        NetworkServerSettingIDs.IDLE_TIMEOUT: 60 * 60,
        NetworkClientSettingIDs.SERVER_ADDRESS: "",
        NetworkClientSettingIDs.CONNECTION_TIMEOUT: 10,
        # Integration settings
        IntegrationSettingIDs.DEFAULT_ROOT_PATH: "/",
    }
