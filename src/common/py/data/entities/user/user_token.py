from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .user import UserID


@dataclass_json
@dataclass(kw_only=True)
class UserToken:
    """
    A token identifying the currently authenticated user.

    Attributes:
        user_id: The user identifier.
        user_name: The user display name.
        system_id: The user's internal system ID.
        access_id: A well-formatted ID to access user resources.
    """

    user_id: UserID = ""
    user_name: str = ""

    system_id: str = ""
    access_id: str = ""
