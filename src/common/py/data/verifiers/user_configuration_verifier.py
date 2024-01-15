import typing

from .verification_exception import VerificationException
from .verifier import Verifier
from ..entities.connector import Connector, ConnectorInstance
from ..entities.user import UserConfiguration


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
        self._verify_connector_instances()

    def verify_update(self) -> None:
        self._verify_connector_instances()

    def verify_delete(self) -> None:
        pass

    def _verify_connector_instances(self) -> None:
        for instance in self._config.connector_instances:
            self._verify_connector_instance(instance)

    def _verify_connector_instance(self, instance: ConnectorInstance) -> None:
        if instance.instance_id <= 0:
            raise VerificationException("Invalid connector instance ID")

        if instance.name == "":
            raise VerificationException("Missing connector instance name")

        if not instance.connector_id in self._connectors:
            raise VerificationException("Connector instance uses an unknown connector")
