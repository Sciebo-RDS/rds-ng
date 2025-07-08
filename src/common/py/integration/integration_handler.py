import abc

from common.py.component import BackendComponent
from common.py.data.entities.authorization import (
    AuthorizationSettings,
    AuthorizationToken,
)
from common.py.data.entities.user import UserToken
from common.py.services import Service


class IntegrationHandler(abc.ABC):
    """
    Base class for integration handlers.
    """

    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        *,
        user_token: UserToken | None = None,
        auth_token: AuthorizationToken | None = None,
        auth_private: AuthorizationSettings | None = None,
    ):
        """
        Args:
            comp: The global component.
            svc: The service to use for message sending.
            user_token: An optional user token.
            auth_token: An optional authorization token.
            auth_private: Optional private authorization settings.
        """

        self._component = comp
        self._service = svc

        self._user_token = user_token
        self._auth_token = auth_token
        self._auth_private = auth_private

    def _replace_user_token_placeholders(self, s: str) -> str:
        if not self._user_token:
            return s

        s = s.replace("{USER_ID}", self._user_token.user_id)
        s = s.replace("{USER_NAME}", self._user_token.user_name)
        s = s.replace("{SYSTEM_ID}", self._user_token.system_id)
        s = s.replace("{ACCESS_ID}", self._user_token.access_id)
        return s
