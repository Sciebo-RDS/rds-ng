from ..utils.config import SettingID


class ComponentSettingIDs:
    """
    Identifiers for component-specific settings.
    
    Attributes:
        INSTANCE: The component's instance name (value type: ``string``).
    """
    INSTANCE = SettingID("component", "instance")
