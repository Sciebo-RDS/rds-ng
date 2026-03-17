import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

AuthorizationSettingsConfig = typing.Dict[str, typing.Any]


@dataclass_json
@dataclass
class AuthorizationSettings:
    """
    Settings for authorization.

    Attributes:
        strategy: The authorization strategy; if empty, none is used.
        config: The authorization configuration.
    """

    strategy: str = ""
    config: AuthorizationSettingsConfig = field(default_factory=dict)
