from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .....utils import RedirectionTarget


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class OAuth2StrategyPublicConfiguration:
    """
    The OAuth2 strategy public configuration.
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
        redirect_target: int = RedirectionTarget.CURRENT

    server: Server = field(default_factory=Server)
    client: Client = field(default_factory=Client)


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class OAuth2StrategyPrivateConfiguration:
    """
    The OAuth2 strategy private configuration.
    """

    @dataclass_json
    @dataclass(frozen=True, kw_only=True)
    class Client:
        client_secret: str = ""

    client: Client = field(default_factory=Client)


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class OAuth2AuthorizationRequestData:
    """
    OAuth2 authorization request data.

    Attributes:
        token_host: The OAuth2 token host.
        token_endpoint: The OAuth2 token endpoint.
        client_id: The OAuth2 client ID.
        auth_code: The authorization code.
        scope: An optional access scope.
        redirect_url: The redirection URL.
    """

    token_host: str
    token_endpoint: str

    client_id: str
    auth_code: str
    scope: str

    redirect_url: str


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class OAuth2Token:
    """
    OAuth2 access token.

    Attributes:
        access_token: The actual token.
        token_type: The type of the token.
        refresh_token: The refresh token (optional).
    """

    access_token: str
    token_type: str

    refresh_token: str | None


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class OAuth2TokenData:
    """
    OAuth2 additional token data.

    Attributes:
        token_host: The OAuth2 token host.
        token_endpoint: The OAuth2 token endpoint.
        client_id: The OAuth2 client ID.
        scope: An optional access scope.
    """

    token_host: str
    token_endpoint: str

    client_id: str
    scope: str
