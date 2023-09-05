from common.py.utils.config import SettingID


class BackendSettingIDs:
    # pylint: disable=too-few-public-methods
    """
    Identifiers for general backend settings.

    Attributes:
        DRIVER: The driver to use for the backend; possible values are "server", "legacy" and "stub" (value type: ``string``).
    """
    DRIVER = SettingID("backend", "driver")
