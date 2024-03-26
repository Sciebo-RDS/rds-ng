from common.py.utils.config import SettingID


class StorageSettingIDs:
    # pylint: disable=too-few-public-methods
    """
    Identifiers for storage settings.

    Attributes:
        DRIVER: The driver to use for the storage; possible value is currently only "memory" (value type: ``string``).
        DEFAULT_ROOT_PATH: The default root path for resources traversal.
    """
    DRIVER = SettingID("storage", "driver")

    DEFAULT_ROOT_PATH = SettingID("storage", "default_root_path")
