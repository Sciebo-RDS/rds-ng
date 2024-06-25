import typing

from common.py.utils.config import SettingID


def get_connector_settings() -> typing.Dict[SettingID, typing.Any]:
    # pylint: disable=too-few-public-methods
    """
    Gets default values for all settings.

    Returns:
        A dictionary mapping the setting identifiers to their default values.
    """

    from .authorization_setting_ids import (
        AuthorizationSettingIDs,
        OAuth2AuthorizationSettingIDs,
    )

    return {
        # Authorization settings
        AuthorizationSettingIDs.STRATEGY: "",
        # OAuth2 settings
        OAuth2AuthorizationSettingIDs.SERVER_HOST: "",
        OAuth2AuthorizationSettingIDs.SERVER_AUTHORIZATION_ENDPOINT: "",
        OAuth2AuthorizationSettingIDs.SERVER_TOKEN_ENDPOINT: "",
        OAuth2AuthorizationSettingIDs.SERVER_SCOPE: "",
        OAuth2AuthorizationSettingIDs.CLIENT_ID: "",
        OAuth2AuthorizationSettingIDs.CLIENT_REDIRECT_URL: "",
    }
