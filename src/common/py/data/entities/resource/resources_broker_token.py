import typing
from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class ResourcesBrokerToken:
    """
    A token identifying the resources broker assigned to a user.

    Attributes:
        broker: The broker identifier.
        config: The broker configuration.
    """

    broker: str
    config: typing.Dict[str, typing.Any]
