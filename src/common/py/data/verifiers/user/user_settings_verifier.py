import typing

from ..connector import (
    ConnectorInstanceVerifier,
)
from .. import Verifier
from ...entities.connector import Connector
from ...entities.user import UserSettings


class UserSettingsVerifier(Verifier):
    """
    Verifies user settings.
    """

    def __init__(self, settings: UserSettings, *, connectors: typing.List[Connector]):
        self._settings = settings

        self._connectors = connectors

    def verify_create(self) -> None:
        for instance in self._settings.connector_instances:
            ConnectorInstanceVerifier(
                instance, connectors=self._connectors
            ).verify_create()

    def verify_update(self) -> None:
        for instance in self._settings.connector_instances:
            ConnectorInstanceVerifier(
                instance, connectors=self._connectors
            ).verify_update()

    def verify_delete(self) -> None:
        for instance in self._settings.connector_instances:
            ConnectorInstanceVerifier(
                instance, connectors=self._connectors
            ).verify_delete()
