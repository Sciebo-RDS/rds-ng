from common.py.utils.config import SettingID


class TransmissionSettingIDs:
    # pylint: disable=too-few-public-methods
    """
    Identifiers for transmission settings.

    Attributes:
        MAX_ATTEMPTS: The maximum number of transmission operation attempts (value type: ``int``).
        ATTEMPTS_DELAY: The delay (in seconds) between transmission operation attempts (value type: ``float``).
    """
    MAX_ATTEMPTS = SettingID("transmission", "max_attempts")
    ATTEMPTS_DELAY = SettingID("transmission", "attempts_delay")
