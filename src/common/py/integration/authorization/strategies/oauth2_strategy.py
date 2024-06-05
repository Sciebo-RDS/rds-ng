import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .authorization_strategy import AuthorizationStrategy
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


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class OAuth2AuthorizationRequestData:
    """
    OAuth2 authorization request data.

    Attributes:
        token_endpoint: The OAuth2 token endpoint.
        client_id: The OAuth2 client ID.
        auth_code: The authorization code.
        redirect_url: The redirection URL.
    """

    token_endpoint: str

    client_id: str
    auth_code: str

    redirect_url: str


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

        pass

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
