from .. import Verifier, VerificationException
from ...entities.connector import Connector


class ConnectorVerifier(Verifier):
    """
    Verifies a connector.
    """

    def __init__(self, connector: Connector):
        self._connector = connector

    def verify_create(self) -> None:
        self._verify_id()
        self._verify_name()

    def verify_update(self) -> None:
        self._verify_id()
        self._verify_name()

    def verify_delete(self) -> None:
        self._verify_id()

    def _verify_id(self) -> None:
        if self._connector.connector_id == "":
            raise VerificationException("Invalid connector ID")

    def _verify_name(self) -> None:
        if self._connector.name == "":
            raise VerificationException("Missing connector name")
