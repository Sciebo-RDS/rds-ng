import typing

from .. import Verifier, VerificationException
from ...entities.connector import Connector, ConnectorInstance


class ConnectorInstanceVerifier(Verifier):
    """
    Verifies a connector instance.
    """

    def __init__(
        self, instance: ConnectorInstance, *, connectors: typing.List[Connector]
    ):
        self._instance = instance

        self._connectors = connectors

    def verify_create(self) -> None:
        self._verify_id()
        self._verify_name()
        self._verify_connector()

    def verify_update(self) -> None:
        self._verify_id()
        self._verify_name()
        self._verify_connector()

    def verify_delete(self) -> None:
        self._verify_id()

    def _verify_id(self) -> None:
        if self._instance.instance_id <= 0:
            raise VerificationException("Invalid connector instance ID")

    def _verify_name(self) -> None:
        if self._instance.name == "":
            raise VerificationException("Missing connector instance name")

    def _verify_connector(self) -> None:
        from ...entities.connector import find_connector_by_id

        if find_connector_by_id(self._connectors, self._instance.connector_id) is None:
            raise VerificationException("Connector instance uses an unknown connector")
