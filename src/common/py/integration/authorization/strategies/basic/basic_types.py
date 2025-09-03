from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class BasicStrategyConfiguration:
    """
    The Basic strategy configuration.

    Attributes:
        user_id_label: The display label of the user ID.
        user_id_optional: Whether the user ID is optional.
        user_password_label: The display label of the user password.
        user_password_optional: Whether the password is optional.
        help_link: An optional link for external help.
    """

    user_id_label: str
    user_id_optional: bool
    user_password_label: str
    user_password_optional: bool

    help_link: str


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class BasicAuthorizationRequestData:
    """
    Basic authorization request data.

    Attributes:
        user_id: The user ID/name.
        user_password: The user password/token.
    """

    user_id: str
    user_password: str


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class BasicToken:
    """
    Basic access token.

    Attributes:
        user_id: The user ID/name.
        user_password: The user password/token.
    """

    user_id: str
    user_password: str
