import typing

from common.py.data.entities.authorization import AuthorizationSettings


class AuthorizationSettingsStore:
    """
    Class to store volatile authorization settings.
    """

    def __init__(self):
        self._settings: typing.Dict[str, AuthorizationSettings] = {}

    def store_settings(self, key: str, settings: AuthorizationSettings) -> None:
        """
        Stores authorization settings.

        Args:
            key: The key under which to store.
            settings: The settings to store.
        """
        self._settings[key] = settings

    def get_settings(self, key: str) -> AuthorizationSettings | None:
        """
        Retrieves stored authorization settings.

        Args:
            key: The key under which to look.

        Returns:
            The stored settings or *None* otherwise.
        """
        return self._settings[key] if key in self._settings else None
