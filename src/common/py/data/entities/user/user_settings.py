import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from ..connector import ConnectorInstance


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class UserSettings:
    """
    User settings (i.e., the settings a user configures in the UI) data.

    Attributes:
        connector_instances: A list of all configured connector instances.
    """

    connector_instances: typing.List[ConnectorInstance] = field(default_factory=list)
