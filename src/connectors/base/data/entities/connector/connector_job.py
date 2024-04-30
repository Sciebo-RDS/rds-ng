from dataclasses import dataclass

from dataclasses_json import dataclass_json

from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.project import Project


@dataclass_json
@dataclass(kw_only=True)
class ConnectorJob:
    """
    Data class for jobs executed by a connector.

    Attributes:
        project: The project.
        connector_instance: The connector instance ID.
    """

    project: Project
    connector_instance: ConnectorInstanceID
