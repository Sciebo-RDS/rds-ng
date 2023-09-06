import typing

from common.py.utils.config import SettingID


def get_gate_settings() -> typing.Dict[SettingID, typing.Any]:
    # pylint: disable=too-few-public-methods
    """
    Gets default values for all gate settings.

    Returns:
        A dictionary mapping the setting identifiers to their default values.
    """
    from gate.settings import BackendSettingIDs

    return {
        BackendSettingIDs.DRIVER: "",
    }
