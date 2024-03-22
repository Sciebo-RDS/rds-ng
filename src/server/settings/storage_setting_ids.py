from common.py.utils.config import SettingID


class StorageSettingIDs:
    # pylint: disable=too-few-public-methods
    """
    Identifiers for storage settings.

    Attributes:
        DRIVER: The driver to use for the storage; possible value is currently only "memory" (value type: ``string``).
    """
    DRIVER = SettingID("storage", "driver")
