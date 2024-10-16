import abc
import time
import typing
from enum import auto, Flag

from .. import AuthorizationRequestPayload
from ... import IntegrationHandler
from ....component import BackendComponent
from ....data.entities.authorization import AuthorizationToken
from ....data.entities.user import UserID, UserToken
from ....services import Service


class AuthorizationStrategy(IntegrationHandler):
    """
    Base class for all authorization strategies.

    Notes:
        Strategies report errors through raising exceptions (usually *RuntimeError*).
    """

    class ContentType(Flag):
        """
        Flags describing what contents the strategy provides.
        """

        AUTH_TOKEN = auto()
        AUTH_LOGIN = auto()
        AUTH_PASSWORD = auto()

    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        strategy: str,
        *,
        contents: ContentType,
        user_token: UserToken | None = None,
        auth_token: AuthorizationToken | None = None,
    ):
        """
        Args:
            comp: The global component.
            svc: The service used to send messages through.
            strategy: The strategy identifier.
            contents: The contents this strategy provides.
            user_token: An optional user token.
            auth_token: An optional authorization token.
        """
        super().__init__(comp, svc, user_token=user_token, auth_token=auth_token)

        self._strategy = strategy
        self._contents = contents

    @abc.abstractmethod
    def request_authorization(
        self,
        user_id: UserID,
        payload: AuthorizationRequestPayload,
        request_data: typing.Any,
    ) -> AuthorizationToken: ...

    @abc.abstractmethod
    def refresh_authorization(self, token: AuthorizationToken) -> None: ...

    def provides_token_content(self, content: ContentType) -> bool:
        """
        Checks if a certain content type is provided by this strategy.

        Args:
            content: The content type.
        """
        return content in self._contents

    def get_token_content(
        self, token: AuthorizationToken, content: ContentType
    ) -> typing.Any:
        """
        Retrieves the token content of the specified type.

        Args:
            token: The authorization token.
            content: The content type.

        Returns:
            The token content or **None** in case of any errors.
        """
        if token is None or content not in self._contents:
            return None

        try:
            return self._get_token_content(token, content)
        except:  # pylint: disable=bare-except
            return None

    def _update_token_refresh_state(
        self, token: AuthorizationToken, *, reset: bool = False
    ) -> None:
        token.timestamp = time.time()

        if reset:
            token.state = AuthorizationToken.TokenState.VALID
            token.refresh_attempts = 0
        else:
            # This needs to be reset if and only if the refresh succeeds
            token.state = AuthorizationToken.TokenState.INVALID
            token.refresh_attempts += 1

    @abc.abstractmethod
    def _get_token_content(
        self, token: AuthorizationToken, content: ContentType
    ) -> typing.Any: ...

    def _get_config_value(self, key: str, default: typing.Any) -> typing.Any:
        from ....utils.config import SettingID

        setting_id = SettingID(f"authorization.{self._strategy}", key)
        return self._component.data.config.value_with_default(setting_id, default)

    @property
    def strategy(self) -> str:
        """
        The strategy identifier.
        """
        return self._strategy

    @property
    def contents(self) -> ContentType:
        """
        The content flags.
        """
        return self._contents
