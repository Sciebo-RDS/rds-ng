import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .authorization_strategy import AuthorizationStrategy
from ....component import BackendComponent
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
        auth_code: The authorization code.
        token_endpoint: The OAuth2 token endpoint.
    """

    auth_code: str
    token_endpoint: str


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


def create_oauth2_strategy(
    comp: BackendComponent, svc: Service, config: typing.Dict[str, typing.Any]
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
    oauth2_config = typing.cast(OAuth2Configuration, config)

    # Verify the passed configuration

    return OAuth2Strategy(comp, svc, oauth2_config)
