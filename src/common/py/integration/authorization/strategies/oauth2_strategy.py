import json
import time
import typing
from dataclasses import dataclass

import requests
from dataclasses_json import dataclass_json

from .authorization_strategy import AuthorizationStrategy
from .oauth2_types import OAuth2Token, OAuth2AuthorizationRequestData, OAuth2TokenData
from ....component import BackendComponent
from ....data.entities.authorization import AuthorizationToken
from ....data.entities.user import UserID
from ....services import Service


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class OAuth2Configuration:
    """
    The OAuth2 strategy configuration.
    """


class OAuth2Strategy(AuthorizationStrategy):
    """
    OAuth2 authorization strategy.
    """

    Strategy: str = "oauth2"

    def __init__(
        self, comp: BackendComponent, svc: Service, config: OAuth2Configuration
    ):
        super().__init__(comp, svc, OAuth2Strategy.Strategy)

        self._config = config

    def request_authorization(
        self, user_id: UserID, auth_id: str, request_data: typing.Any
    ) -> AuthorizationToken:
        oauth2_data = self._get_request_data(request_data)
        client_secret = self._get_client_secret(auth_id)

        response = requests.post(
            oauth2_data.token_endpoint,
            data={
                "grant_type": "authorization_code",
                "client_id": oauth2_data.client_id,
                "client_secret": client_secret,
                "code": oauth2_data.auth_code,
                "redirect_uri": oauth2_data.redirect_url,
            },
        )

        if response.status_code == 200:
            resp_data = response.json()
            try:
                self._verify_oauth2_token_data(resp_data)

                return AuthorizationToken(
                    user_id=user_id,
                    auth_id=auth_id,
                    expiration_timestamp=(
                        time.time() + resp_data["expires_in"]
                        if "expires_in" in resp_data
                        else 0
                    ),
                    strategy=self.strategy,
                    token=OAuth2Token(
                        access_token=resp_data["access_token"],
                        token_type=resp_data["token_type"],
                        refresh_token=resp_data["refresh_token"],
                    ),
                    data=OAuth2TokenData(
                        token_endpoint=oauth2_data.token_endpoint,
                        client_id=oauth2_data.client_id,
                    ),
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                raise RuntimeError(f"Invalid OAuth2 token received: {exc}")
        else:
            raise RuntimeError(
                f"Unable to request an access token: {response.text}"
            )  # TODO: Proper err

    def _get_request_data(
        self, request_data: typing.Any
    ) -> OAuth2AuthorizationRequestData:
        oauth2_data = OAuth2AuthorizationRequestData.from_dict(request_data)

        # Verify the request data
        if oauth2_data.token_endpoint == "":
            raise RuntimeError("Missing token endpoint")
        if oauth2_data.client_id == "":
            raise RuntimeError("Missing client ID")
        if oauth2_data.auth_code == "":
            raise RuntimeError("Missing authentication code")
        if oauth2_data.redirect_url == "":
            raise RuntimeError("Missing redirection URL")

        return oauth2_data

    def _get_client_secret(self, auth_id: str) -> str:
        client_secret = self._get_config_value(f"secrets.{auth_id}", "")

        # Verify the secret
        if client_secret == "":
            raise RuntimeError(f"Missing OAuth2 client secret for {auth_id}")

        return client_secret

    def _verify_oauth2_token_data(self, data: typing.Dict[str, typing.Any]) -> None:
        if "access_token" not in data or data["access_token"] == "":
            raise RuntimeError("Missing access token")
        if "token_type" not in data or data["token_type"] == "":
            raise RuntimeError("Missing token type")
        if "refresh_token" not in data or data["refresh_token"] == "":
            raise RuntimeError("Missing refresh token")


def create_oauth2_strategy(
    comp: BackendComponent, svc: Service, config: typing.Any
) -> OAuth2Strategy:
    """
    Creates a new OAuth2 strategy instance, automatically configuring it.

    Args:
        comp: The main component.
        svc: The service to use for message sending.
        config: The strategy configuration.

    Returns:
        The newly created strategy.
    """
    if not isinstance(config, OAuth2Configuration):
        raise RuntimeError("Invalid configuration passed for OAuth2")

    oauth2_config = typing.cast(OAuth2Configuration, config)

    return OAuth2Strategy(comp, svc, oauth2_config)
