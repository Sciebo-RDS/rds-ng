from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class BearerStrategyConfiguration:
    """
    The Bearer strategy configuration.

    Attributes:
        bearer_label: The display label of the bearer token.
        help_link: An optional link for external help.
    """

    bearer_label: str

    help_link: str


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class BearerAuthorizationRequestData:
    """
    Bearer authorization request data.

    Attributes:
        bearer_token: The bearer token.
    """

    bearer_token: str


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class BearerToken:
    """
    Bearer access token.

    Attributes:
        bearer_token: The bearer token.
    """

    bearer_token: str
