from .verifier import Verifier
from ..entities.user import UserConfiguration


class UserConfigurationVerifier(Verifier):
    """
    Verifies a user configuration.
    """

    def __init__(self, config: UserConfiguration):
        self._config = config

    def verify_create(self) -> None:
        pass

    def verify_update(self) -> None:
        pass

    def verify_delete(self) -> None:
        pass
