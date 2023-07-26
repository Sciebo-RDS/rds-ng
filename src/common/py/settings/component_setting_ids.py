from ..utils.config import SettingID


class ComponentSettingIDs:
    # pylint: disable=too-few-public-methods
    """
    Identifiers for component-specific settings.
    
    Attributes:
        INSTANCE: The component's instance name (value type: ``string``).
    """
    INSTANCE = SettingID("component", "instance")
