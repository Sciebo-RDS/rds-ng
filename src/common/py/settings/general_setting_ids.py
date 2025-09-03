from ..utils.config import SettingID


class GeneralSettingIDs:
    # pylint: disable=too-few-public-methods
    """
    Identifiers for general settings.

    Attributes:
        DEBUG: Whether debug mode should be enabled (value type: ``bool``).
        DEBUG_TRACE: Whether to trace function calls (value type: ``bool``).
    """
    DEBUG = SettingID("general", "debug")
    DEBUG_TRACE = SettingID("general", "debug_trace")
