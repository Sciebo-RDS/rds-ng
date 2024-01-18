from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .connector import ConnectorID

ConnectorInstanceID = int


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class ConnectorInstance:
    """
    A configured connector instance (i.e., a connector the user has added to his configuration).

    Attributes:
        instance_id: The ID of the connector instance.
        connector_id: The assigned connector.
        name: The name of this connector instance.
        description: The instance description.
    """

    instance_id: ConnectorInstanceID

    connector_id: ConnectorID

    name: str
    description: str = ""
