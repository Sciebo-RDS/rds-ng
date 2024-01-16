import typing

from common.py.data.verifiers.connector.connector_instance_verifier import (
    ConnectorInstanceVerifier,
)
from common.py.data.verifiers.verifier import Verifier
from common.py.data.entities.connector import Connector
from common.py.data.entities.user import UserSettings


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
