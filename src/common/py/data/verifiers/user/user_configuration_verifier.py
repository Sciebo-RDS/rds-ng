import typing

from common.py.data.verifiers.connector.connector_instance_verifier import (
    ConnectorInstanceVerifier,
)
from common.py.data.verifiers.verifier import Verifier
from common.py.data.entities.connector import Connector
from common.py.data.entities.user import UserConfiguration


class UserConfigurationVerifier(Verifier):
    """
    Verifies a user configuration.
    """

    def __init__(
        self, config: UserConfiguration, *, connectors: typing.List[Connector]
    ):
        self._config = config

        self._connectors = connectors

    def verify_create(self) -> None:
        for instance in self._config.connector_instances:
            ConnectorInstanceVerifier(
                instance, connectors=self._connectors
            ).verify_create()

    def verify_update(self) -> None:
        for instance in self._config.connector_instances:
            ConnectorInstanceVerifier(
                instance, connectors=self._connectors
            ).verify_update()

    def verify_delete(self) -> None:
        for instance in self._config.connector_instances:
            ConnectorInstanceVerifier(
                instance, connectors=self._connectors
            ).verify_delete()
