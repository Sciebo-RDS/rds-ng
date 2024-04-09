from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .user import UserID


@dataclass_json
@dataclass(kw_only=True)
class UserToken:
    """
    A token identifying the currently authenticated user.
    """

    user_id: UserID = ""
    user_name: str = ""
