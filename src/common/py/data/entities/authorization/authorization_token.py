import typing
from dataclasses import dataclass, field
from enum import StrEnum

from dataclasses_json import dataclass_json

# Avoid some cyclic dependencies
if typing.TYPE_CHECKING:
    from ..user import UserID
else:
    UserID = str

AuthorizationTokenID = typing.Tuple[UserID, str]


@dataclass_json
@dataclass(kw_only=True)
class AuthorizationToken:
    """
    A token holding authorization information for an external system.

    Attributes:
        user_id: The user identifier.
        auth_id: The ID of this token.
        auth_type: The token type.
        auth_issuer: The entity that requires the authorization.
        auth_bearer: The bearer that will be authorized against.
        expiration_timestamp: Timestamp when the token becomes invalid; a value of 0 means that the token never becomes invalid.
        strategy: The token strategy (e.g., OAuth2).
        token: The actual token data.
        data: Arbitrary strategy data (usually configuration).
    """

    class TokenType(StrEnum):
        """
        Various token types.
        """

        INVALID = ""

        HOST = "host"
        CONNECTOR = "connector"

    user_id: UserID

    auth_id: str
    auth_type: str
    auth_issuer: str
    auth_bearer: str

    expiration_timestamp: float

    strategy: str
    token: typing.Dict[str, typing.Any]
    data: typing.Dict[str, typing.Any]

    def __post_init__(self):
        self._convert_dataclasses()

    def __setattr__(self, prop, val):
        if hasattr(val, "to_dict"):
            # Automatically convert JSON dataclasses to dictionaries
            super().__setattr__(prop, val.to_dict())
        else:
            super().__setattr__(prop, val)

    def _convert_dataclasses(self) -> None:
        # Automatically convert JSON dataclasses to dictionaries
        if hasattr(self.token, "to_dict"):
            self.token = self.token.to_dict()
        if hasattr(self.data, "to_dict"):
            self.data = self.data.to_dict()
