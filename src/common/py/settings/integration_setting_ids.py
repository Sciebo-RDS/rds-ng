from ..utils.config import SettingID


class IntegrationSettingIDs:
    # pylint: disable=too-few-public-methods
    """
    Identifiers for integration settings.

    Attributes:
        DEFAULT_ROOT_PATH: The default root path for resources (value type: ``string``).
    """
    DEFAULT_ROOT_PATH = SettingID("integration", "default_root_path")
