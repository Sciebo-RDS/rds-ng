from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class UserToken:
    """
    A token identifying the currently authenticated user.
    """

    user_id: str = ""
    user_name: str = ""
