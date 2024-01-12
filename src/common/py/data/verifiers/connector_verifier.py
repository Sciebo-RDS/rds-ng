from .verification_exception import VerificationException
from .verifier import Verifier
from ..entities.connector import Connector
from ...component import ComponentType


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
        if (
            self._connector.connector_id.type != ComponentType.CONNECTOR
            or self._connector.connector_id.unit == ""
            or self._connector.connector_id.instance is not None
        ):
            raise VerificationException("Invalid connector ID")

    def _verify_name(self) -> None:
        if self._connector.name == "":
            raise VerificationException("Missing connector name")
