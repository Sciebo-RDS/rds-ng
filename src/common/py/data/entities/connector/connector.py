from dataclasses import dataclass

from dataclasses_json import dataclass_json

ConnectorID = str


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class Connector:
    """
    Data for a single **Connector**.

    Attributes:
        connector_id: The unique connector identifier.
        name: The name of the connector.
        description: An optional connector description.
    """

    connector_id: ConnectorID

    name: str
    description: str
