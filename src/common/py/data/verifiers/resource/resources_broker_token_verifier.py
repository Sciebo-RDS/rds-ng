from .. import Verifier, VerificationException
from ...entities.resource import ResourcesBrokerToken


class ResourcesBrokerTokenVerifier(Verifier):
    """
    Verifies a resources broker token.
    """

    def __init__(self, token: ResourcesBrokerToken):
        self._token = token

    def verify_create(self) -> None:
        self._verify_broker()

    def verify_update(self) -> None:
        self._verify_broker()

    def verify_delete(self) -> None:
        self._verify_broker()

    def _verify_broker(self) -> None:
        if self._token.broker == "":
            raise VerificationException("Invalid broker ID")
