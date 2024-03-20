from common.py.utils.config import SettingID


class BackendSettingIDs:
    # pylint: disable=too-few-public-methods
    """
    Identifiers for general backend settings.

    Attributes:
        DRIVER: The driver to use for the backend; possible values are "server", "legacy" and "stub" (value type: ``string``).
        DEFAULT_ROOT_PATH: The default root path for resources traversal.
    """
    DRIVER = SettingID("backend", "driver")

    DEFAULT_ROOT_PATH = SettingID("backend", "default_root_path")
