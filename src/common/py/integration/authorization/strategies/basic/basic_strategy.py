import time
import typing

from .basic_types import (
    BasicAuthorizationRequestData,
    BasicStrategyConfiguration,
    BasicToken,
)
from ..authorization_strategy import AuthorizationStrategy
from ... import AuthorizationRequestPayload
from .....component import BackendComponent
from .....data.entities.authorization import AuthorizationSettings, AuthorizationToken
from .....data.entities.user import UserID, UserToken
from .....services import Service


class BasicStrategy(AuthorizationStrategy):
    """
    Basic authorization strategy.
    """

    Strategy: str = "basic"

    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        *,
        user_token: UserToken | None = None,
        auth_token: AuthorizationToken | None = None,
        auth_public: AuthorizationSettings | None = None,
        auth_private: AuthorizationSettings | None = None,
    ):
        super().__init__(
            comp,
            svc,
            BasicStrategy.Strategy,
            contents=(
                AuthorizationStrategy.ContentType.AUTH_LOGIN
                | AuthorizationStrategy.ContentType.AUTH_PASSWORD
            ),
            user_token=user_token,
            auth_token=auth_token,
            auth_public=auth_public,
            auth_private=auth_private,
        )

    def request_authorization(
        self,
        user_id: UserID,
        payload: AuthorizationRequestPayload,
        request_data: typing.Any,
    ) -> AuthorizationToken:
        return AuthorizationToken(
            user_id=user_id,
            auth_id=payload.auth_id,
            auth_type=payload.auth_type,
            auth_issuer=payload.auth_issuer,
            auth_issuer_url=payload.auth_issuer_url,
            auth_bearer=payload.auth_bearer,
            state=AuthorizationToken.TokenState.VALID,
            timestamp=time.time(),
            expiration_timestamp=0,
            refresh_attempts=0,
            strategy=self.strategy,
            token=typing.cast(
                typing.Dict[any, str], self._create_basic_token(request_data)
            ),
            data={},
        )

    def refresh_authorization(self, token: AuthorizationToken) -> None:
        # We simply reset the token so it continues to be valid
        super()._update_token_refresh_state(token, reset=True)

    def _get_token_content(
        self, token: AuthorizationToken, content: AuthorizationStrategy.ContentType
    ) -> typing.Any:
        basic_token = self._get_basic_data_from_token(token)

        if content == AuthorizationStrategy.ContentType.AUTH_LOGIN:
            return basic_token.user_id
        elif content == AuthorizationStrategy.ContentType.AUTH_PASSWORD:
            return basic_token.user_password

        return None

    def _create_basic_token(self, request_data: typing.Any) -> BasicToken:
        config = self._get_public_configuration(BasicStrategyConfiguration)

        basic_data: BasicAuthorizationRequestData = (
            BasicAuthorizationRequestData.from_dict(request_data)
        )

        if not config.user_id_optional and basic_data.user_id == "":
            raise RuntimeError("Missing user ID")
        if not config.user_password_optional and basic_data.user_password == "":
            raise RuntimeError("Missing user password")

        return BasicToken(
            user_id=basic_data.user_id, user_password=basic_data.user_password
        )

    def _get_basic_data_from_token(self, token: AuthorizationToken) -> BasicToken:
        return BasicToken.from_dict(token.token)


def create_basic_strategy(
    comp: BackendComponent,
    svc: Service,
    *,
    user_token: UserToken | None = None,
    auth_token: AuthorizationToken | None = None,
    auth_public: AuthorizationSettings | None = None,
    auth_private: AuthorizationSettings | None = None,
) -> BasicStrategy:
    """
    Creates a new OAuth2 strategy instance.

    Args:
        comp: The main component.
        svc: The service to use for message sending.
        user_token: An optional user token.
        auth_token: An optional authorization token.
        auth_public: Optional public authorization settings.
        auth_private: Optional private authorization settings.

    Returns:
        The newly created strategy.
    """
    return BasicStrategy(
        comp,
        svc,
        user_token=user_token,
        auth_token=auth_token,
        auth_public=auth_public,
        auth_private=auth_private,
    )
