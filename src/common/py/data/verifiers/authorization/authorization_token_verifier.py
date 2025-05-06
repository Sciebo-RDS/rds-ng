from .. import Verifier, VerificationException
from ...entities.authorization import AuthorizationToken


class AuthorizationTokenVerifier(Verifier):
    """
    Verifies an authorization token.
    """

    def __init__(self, token: AuthorizationToken):
        self._token = token

    def verify_create(self) -> None:
        self._verify_user_id()
        self._verify_auth_id()
        self._verify_strategy()
        self._verify_token()

    def verify_update(self) -> None:
        self._verify_user_id()
        self._verify_auth_id()
        self._verify_strategy()
        self._verify_token()

    def verify_delete(self) -> None:
        self._verify_user_id()
        self._verify_auth_id()

    def _verify_user_id(self) -> None:
        if self._token.user_id == "":
            raise VerificationException("Invalid user ID")

    def _verify_auth_id(self) -> None:
        if self._token.auth_id == "":
            raise VerificationException("Invalid authorization ID")

    def _verify_strategy(self) -> None:
        if self._token.strategy == "":
            raise VerificationException("Invalid strategy")

    def _verify_token(self) -> None:
        if self._token.token is None:
            raise VerificationException("Invalid token")
