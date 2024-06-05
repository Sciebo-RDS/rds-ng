import typing
from dataclasses import dataclass
from enum import StrEnum

from dataclasses_json import dataclass_json

from ..user import UserID

AuthorizationTokenID = typing.Tuple[UserID, str]


@dataclass_json
@dataclass(kw_only=True)
class AuthorizationToken:
    """
    A token holding authorization information for an external system.

    Attributes:
        user_id: The user identifier.
        auth_id: The id of this token.
        expiration_timestamp: Timestamp when the token becomes invalid; a value of 0 means that the token never becomes invalid.
        strategy: The token strategy (e.g., OAuth2).
        token: The actual token data.
        data: Arbitrary strategy data (usually configuration).
    """

    class TokenType(StrEnum):
        """
        Various token types.
        """

        HOST = "host"
        CONNECTOR = "connector"

    user_id: UserID
    auth_id: str

    expiration_timestamp: float = 0.0

    strategy: str
    token: any
    data: any
