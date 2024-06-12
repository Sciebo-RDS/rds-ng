import abc
import typing
from enum import auto, IntFlag, Flag

from ....component import BackendComponent
from ....data.entities.authorization import AuthorizationToken
from ....data.entities.user import UserID
from ....services import Service


class AuthorizationStrategy(abc.ABC):
    """
    Base class for all authorization strategies.

    Notes:
        Strategies report errors through raising exceptions (usually *RuntimeError*).
    """

    class ContentType(Flag):
        """
        Flags describing what contents the strategy provides.
        """

        AUTH_CREDENTIALS = auto()
        AUTH_TOKEN = auto()

    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        strategy: str,
        contents: ContentType,
    ):
        """
        Args:
            comp: The global component.
            svc: The service used to send messages through.
            strategy: The strategy identifier.
        """
        self._component = comp
        self._service = svc

        self._strategy = strategy
        self._contents = contents

    @abc.abstractmethod
    def request_authorization(
        self, user_id: UserID, auth_id: str, request_data: typing.Any
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
        except:
            return None

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
