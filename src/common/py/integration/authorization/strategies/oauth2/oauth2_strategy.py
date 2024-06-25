import time
import typing
import urllib.parse
from dataclasses import dataclass, field
from http import HTTPStatus

import requests
from dataclasses_json import dataclass_json

from .oauth2_types import OAuth2Token, OAuth2AuthorizationRequestData, OAuth2TokenData
from .oauth2_utils import format_oauth2_error_response
from ..authorization_strategy import AuthorizationStrategy
from ... import AuthorizationRequestPayload
from .....component import BackendComponent
from .....data.entities.authorization import AuthorizationToken
from .....data.entities.user import UserID, UserToken
from .....services import Service


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class OAuth2StrategyConfiguration:
    """
    The OAuth2 strategy configuration.
    """

    @dataclass_json
    @dataclass(frozen=True, kw_only=True)
    class Server:
        host: str = ""
        authorization_endpoint: str = ""
        token_endpoint: str = ""
        scope: str = ""

    @dataclass_json
    @dataclass(frozen=True, kw_only=True)
    class Client:
        client_id: str = ""
        redirect_url: str = ""

    server: Server = field(default_factory=Server)
    client: Client = field(default_factory=Client)


class OAuth2Strategy(AuthorizationStrategy):
    """
    OAuth2 authorization strategy.
    """

    Strategy: str = "oauth2"

    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        *,
        user_token: UserToken | None = None,
        auth_token: AuthorizationToken | None = None,
    ):
        from .....settings import NetworkSettingIDs

        super().__init__(
            comp,
            svc,
            OAuth2Strategy.Strategy,
            contents=AuthorizationStrategy.ContentType.AUTH_TOKEN,
            user_token=user_token,
            auth_token=auth_token,
        )

        self._request_timeout = comp.data.config.value(
            NetworkSettingIDs.EXTERNAL_REQUESTS_TIMEOUT
        )

    def request_authorization(
        self,
        user_id: UserID,
        payload: AuthorizationRequestPayload,
        request_data: typing.Any,
    ) -> AuthorizationToken:
        oauth2_data = self._get_oauth2_request_data(request_data)
        client_secret = self._get_client_secret(payload.auth_bearer)

        response = requests.post(
            urllib.parse.urljoin(oauth2_data.token_host, oauth2_data.token_endpoint),
            data={
                "grant_type": "authorization_code",
                "client_id": oauth2_data.client_id,
                "client_secret": client_secret,
                "scope": oauth2_data.scope,
                "code": oauth2_data.auth_code,
                "redirect_uri": oauth2_data.redirect_url,
            },
            timeout=self._request_timeout,
        )

        if response.status_code == HTTPStatus.OK:
            resp_data = response.json()
            try:
                self._verify_oauth2_token_data(resp_data)

                return AuthorizationToken(
                    user_id=user_id,
                    auth_id=payload.auth_id,
                    auth_type=payload.auth_type,
                    auth_issuer=payload.auth_issuer,
                    auth_bearer=payload.auth_bearer,
                    expiration_timestamp=self._get_expiration_timestamp(resp_data),
                    strategy=self.strategy,
                    token=self._create_oauth2_token(resp_data),
                    data=OAuth2TokenData(
                        token_host=oauth2_data.token_host,
                        token_endpoint=oauth2_data.token_endpoint,
                        client_id=oauth2_data.client_id,
                        scope=oauth2_data.scope,
                    ),
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                raise RuntimeError(f"Invalid OAuth2 token received: {exc}")
        else:
            raise RuntimeError(
                f"Unable to request access token: {format_oauth2_error_response(response)}"
            )

    def refresh_authorization(self, token: AuthorizationToken) -> None:
        oauth2_token, oauth2_data = self._get_oauth2_data_from_token(token)
        client_secret = self._get_client_secret(token.auth_bearer)

        if oauth2_token.refresh_token is None:
            raise RuntimeError("Tried to refresh without a refresh token")

        response = requests.post(
            urllib.parse.urljoin(oauth2_data.token_host, oauth2_data.token_endpoint),
            data={
                "grant_type": "refresh_token",
                "client_id": oauth2_data.client_id,
                "client_secret": client_secret,
                "scope": oauth2_data.scope,
                "refresh_token": oauth2_token.refresh_token,
            },
            timeout=self._request_timeout,
        )

        if response.status_code == HTTPStatus.OK:
            resp_data = response.json()
            try:
                self._verify_oauth2_token_data(resp_data)

                token.expiration_timestamp = self._get_expiration_timestamp(resp_data)
                token.token = self._create_oauth2_token(resp_data)
            except Exception as exc:  # pylint: disable=broad-exception-caught
                raise RuntimeError(f"Invalid OAuth2 token received: {exc}")
        else:
            raise RuntimeError(
                f"Unable to refresh access token: {format_oauth2_error_response(response)}"
            )

    def _get_token_content(
        self, token: AuthorizationToken, content: AuthorizationStrategy.ContentType
    ) -> typing.Any:
        # We only support a single content type, so no need to distinguish
        oauth2_token, _ = self._get_oauth2_data_from_token(token)
        return oauth2_token.access_token

    def _create_oauth2_token(self, resp_data) -> OAuth2Token:
        return OAuth2Token(
            access_token=resp_data["access_token"],
            token_type=resp_data["token_type"],
            refresh_token=(
                resp_data["refresh_token"] if "refresh_token" in resp_data else None
            ),
        )

    def _get_oauth2_request_data(
        self, request_data: typing.Any
    ) -> OAuth2AuthorizationRequestData:
        oauth2_data: OAuth2AuthorizationRequestData = (
            OAuth2AuthorizationRequestData.from_dict(request_data)
        )

        # Verify the request data
        if oauth2_data.token_host == "":
            raise RuntimeError("Missing token host")
        if oauth2_data.token_endpoint == "":
            raise RuntimeError("Missing token endpoint")
        if oauth2_data.client_id == "":
            raise RuntimeError("Missing client ID")
        if oauth2_data.auth_code == "":
            raise RuntimeError("Missing authentication code")
        if oauth2_data.redirect_url == "":
            raise RuntimeError("Missing redirection URL")

        return oauth2_data

    def _get_oauth2_data_from_token(
        self, token: AuthorizationToken
    ) -> typing.Tuple[OAuth2Token, OAuth2TokenData]:
        oauth2_token: OAuth2Token = OAuth2Token.from_dict(token.token)
        oauth2_data: OAuth2TokenData = OAuth2TokenData.from_dict(token.data)
        return oauth2_token, oauth2_data

    def _get_client_secret(self, auth_bearer: str) -> str:
        client_secret = self._get_config_value(f"secrets.{auth_bearer}", "")

        # Verify the secret
        if client_secret == "":
            raise RuntimeError(f"Missing OAuth2 client secret for {auth_bearer}")

        return client_secret

    def _get_expiration_timestamp(
        self, resp_data: typing.Dict[str, typing.Any]
    ) -> float:
        # We reduce the lifespan by 10% to refresh tokens early on
        return (
            time.time() + (resp_data["expires_in"] * 0.9)
            if "expires_in" in resp_data
            else 0
        )

    def _verify_oauth2_token_data(self, data: typing.Dict[str, typing.Any]) -> None:
        if "access_token" not in data or data["access_token"] == "":
            raise RuntimeError("Missing access token")
        if "token_type" not in data or data["token_type"] == "":
            raise RuntimeError("Missing token type")


def create_oauth2_strategy(
    comp: BackendComponent,
    svc: Service,
    *,
    user_token: UserToken | None = None,
    auth_token: AuthorizationToken | None = None,
) -> OAuth2Strategy:
    """
    Creates a new OAuth2 strategy instance.

    Args:
        comp: The main component.
        svc: The service to use for message sending.
        user_token: An optional user token.
        auth_token: An optional authorization token.

    Returns:
        The newly created strategy.
    """
    return OAuth2Strategy(comp, svc, user_token=user_token, auth_token=auth_token)
