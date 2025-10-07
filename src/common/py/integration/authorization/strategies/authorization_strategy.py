import abc
import time
import typing
from enum import auto, Flag

from .. import AuthorizationRequestPayload
from ... import IntegrationHandler
from ....component import BackendComponent
from ....data.entities.authorization import AuthorizationSettings, AuthorizationToken
from ....data.entities.user import HostID, UserID, UserToken
from ....services import Service

ConfigType = typing.TypeVar("ConfigType")  # pylint: disable=invalid-name


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
        auth_public: AuthorizationSettings | None = None,
        auth_private: AuthorizationSettings | None = None,
    ):
        """
        Args:
            comp: The global component.
            svc: The service used to send messages through.
            strategy: The strategy identifier.
            contents: The contents this strategy provides.
            user_token: An optional user token.
            auth_token: An optional authorization token.
            auth_public: Optional public authorization settings.
            auth_private: Optional private authorization settings.
        """
        super().__init__(
            comp,
            svc,
            user_token=user_token,
            auth_token=auth_token,
            auth_public=auth_public,
            auth_private=auth_private,
        )

        self._strategy = strategy
        self._contents = contents

    @abc.abstractmethod
    def request_authorization(
        self,
        *,
        user_id: UserID,
        host_id: HostID | None,
        payload: AuthorizationRequestPayload,
        request_data: typing.Any,
    ) -> AuthorizationToken: ...

    @abc.abstractmethod
    def refresh_authorization(
        self, token: AuthorizationToken, *, host_id: HostID | None = None
    ) -> None: ...

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

    def _get_config_value(
        self, key: str, default: typing.Any, *, host_id: HostID | None = None
    ) -> typing.Any:
        from ....utils.config import SettingID

        setting_id = SettingID(
            f"{host_id + '.' if host_id is not None else ''}authorization.{self._strategy}",
            key,
        )
        return self._component.data.config.value_with_default(setting_id, default)

    def _get_public_configuration(self, cls: type[ConfigType]) -> ConfigType:
        return (
            cls.from_dict(self._auth_public.config)
            if self._auth_public is not None
            else cls()
        )

    def _get_private_configuration(self, cls: type[ConfigType]) -> ConfigType:
        return (
            cls.from_dict(self._auth_private.config)
            if self._auth_private is not None
            else cls()
        )

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
