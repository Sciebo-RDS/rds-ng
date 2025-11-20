import dataclasses
import time
import typing

from .bearer_types import (
    BearerAuthorizationRequestData,
    BearerStrategyConfiguration,
    BearerToken,
)
from ..authorization_strategy import AuthorizationStrategy
from ... import AuthorizationRequestPayload
from .....component import BackendComponent
from .....data.entities.authorization import AuthorizationSettings, AuthorizationToken
from .....data.entities.user import HostID, UserID, UserToken
from .....services import Service


class BearerStrategy(AuthorizationStrategy):
    """
    Bearer authorization strategy.
    """

    Strategy: str = "bearer"

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
            BearerStrategy.Strategy,
            contents=AuthorizationStrategy.ContentType.AUTH_TOKEN,
            user_token=user_token,
            auth_token=auth_token,
            auth_public=auth_public,
            auth_private=auth_private,
        )

    def request_authorization(
        self,
        *,
        user_id: UserID,
        host_id: HostID,
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
            token=dataclasses.asdict(self._create_bearer_token(request_data)),
            data={},
        )

    def refresh_authorization(
        self, token: AuthorizationToken, *, host_id: HostID | None = None
    ) -> None:
        # We simply reset the token so it continues to be valid
        super()._update_token_refresh_state(token, reset=True)

    def _get_token_content(
        self, token: AuthorizationToken, content: AuthorizationStrategy.ContentType
    ) -> typing.Any:
        # We only support a single content type, so no need to distinguish
        bearer_token = self._get_bearer_data_from_token(token)
        return bearer_token.bearer_token

    def _create_bearer_token(self, request_data: typing.Any) -> BearerToken:
        config = self._get_public_configuration(BearerStrategyConfiguration)

        bearer_data: BearerAuthorizationRequestData = (
            BearerAuthorizationRequestData.from_dict(request_data)
        )

        if bearer_data.bearer_token == "":
            raise RuntimeError("Missing bearer token")

        return BearerToken(bearer_token=bearer_data.bearer_token)

    def _get_bearer_data_from_token(self, token: AuthorizationToken) -> BearerToken:
        return BearerToken.from_dict(token.token)


def create_bearer_strategy(
    comp: BackendComponent,
    svc: Service,
    *,
    user_token: UserToken | None = None,
    auth_token: AuthorizationToken | None = None,
    auth_public: AuthorizationSettings | None = None,
    auth_private: AuthorizationSettings | None = None,
) -> AuthorizationStrategy:
    """
    Creates a new Bearer strategy instance.

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
    return BearerStrategy(
        comp,
        svc,
        user_token=user_token,
        auth_token=auth_token,
        auth_public=auth_public,
        auth_private=auth_private,
    )
