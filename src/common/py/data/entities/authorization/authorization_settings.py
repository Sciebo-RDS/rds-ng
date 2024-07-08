import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json


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
    config: typing.Dict[str, typing.Any] = field(default_factory=dict)
