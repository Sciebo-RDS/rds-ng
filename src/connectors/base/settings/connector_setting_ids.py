from common.py.utils.config import SettingID


class ConnectorSettingIDs:
    # pylint: disable=too-few-public-methods
    """
    Identifiers for connector settings.

    Attributes:
        TARGET: The URL of the connector target (value type: ``string``).
    """
    TARGET = SettingID("connector", "target")
