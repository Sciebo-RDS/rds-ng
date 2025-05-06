from common.py.utils.config import SettingID


class AuthorizationSettingIDs:
    # pylint: disable=too-few-public-methods
    """
    Identifiers for general authorization settings.

    Attributes:
        REFRESH_ATTEMPTS_DELAY: The delay between token refresh attempts in seconds (value type: ``float``).
        REFRESH_ATTEMPTS_LIMIT: The maximum number of refresh attempts before removing a token; 0 disables removal (value type: ``int``).
    """
    REFRESH_ATTEMPTS_DELAY = SettingID("authorization", "refresh_attempts_delay")
    REFRESH_ATTEMPTS_LIMIT = SettingID("authorization", "refresh_attempts_limit")
