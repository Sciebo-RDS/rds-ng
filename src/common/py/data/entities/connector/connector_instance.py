import uuid
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .connector import ConnectorID

ConnectorInstanceID = uuid.UUID


@dataclass_json
@dataclass(kw_only=True)
class ConnectorInstance:
    """
    A configured connector instance (i.e., a connector the user has added to his configuration).

    Attributes:
        instance_id: The ID of the connector instance.
        connector_id: The assigned connector.
        name: The name of this connector instance.
        description: The instance description.
    """

    instance_id: ConnectorInstanceID = field(default_factory=uuid.uuid4)

    connector_id: ConnectorID = ""

    name: str = ""
    description: str = ""
