import typing

from common.py.utils.config import SettingID


def get_server_settings() -> typing.Dict[SettingID, typing.Any]:
    # pylint: disable=too-few-public-methods
    """
    Gets default values for all server settings.

    Returns:
        A dictionary mapping the setting identifiers to their default values.
    """
    return {}
