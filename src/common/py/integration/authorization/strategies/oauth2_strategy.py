from dataclasses import dataclass, field

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class OAuth2AuthorizationRequestData:
    """
    OAuth2 authorization request data.

    Attributes:
        auth: The authorization data.
        endpoints: The OAuth2 server endpoints.
    """

    @dataclass_json
    @dataclass(kw_only=True)
    class Authorization:
        code: str

    @dataclass_json
    @dataclass(kw_only=True)
    class Endpoints:
        token: str

    auth: Authorization = field(default_factory=Authorization)
    endpoints: Endpoints = field(default_factory=Endpoints)
