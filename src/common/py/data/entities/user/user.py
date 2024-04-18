import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from ..connector import ConnectorInstance

UserID = str


@dataclass_json
@dataclass(kw_only=True)
class User:
    """
    A user account.

    Attributes:
        user_id: The user ID.
        name: The (display) name of the user.
        user_settings: The settings of the user.
    """

    @dataclass_json
    @dataclass
    class Settings:
        """
        User settings (i.e., the settings a user configures in the UI) data.

        Attributes:
            connector_instances: A list of all configured connector instances.
        """

        connector_instances: typing.List[ConnectorInstance] = field(
            default_factory=list
        )

    user_id: UserID

    name: str

    user_settings: Settings = field(default_factory=Settings)
