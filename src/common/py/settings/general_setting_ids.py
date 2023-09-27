from ..utils.config import SettingID


class GeneralSettingIDs:
    # pylint: disable=too-few-public-methods
    """
    Identifiers for general settings.

    Attributes:
        DEBUG: Whether debug mode should be enabled (value type: ``bool``).
    """
    DEBUG = SettingID("general", "debug")
