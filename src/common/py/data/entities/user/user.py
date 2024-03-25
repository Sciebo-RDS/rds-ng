from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from common.py.data.entities.user import UserSettings

UserID = str


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class User:
    """
    A user account.

    Attributes:
        user_id: The user ID.
        user_settings: The settings of the user.
    """

    user_id: UserID

    user_settings: UserSettings = field(default_factory=UserSettings)