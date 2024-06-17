import typing

from common.py.utils.config import SettingID


def get_connector_settings() -> typing.Dict[SettingID, typing.Any]:
    # pylint: disable=too-few-public-methods
    """
    Gets default values for all settings.

    Returns:
        A dictionary mapping the setting identifiers to their default values.
    """

    return {}
