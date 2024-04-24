from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .project import ProjectID
from ..connector import ConnectorInstanceID


@dataclass_json
@dataclass(kw_only=True)
class ProjectJob:
    """
    A project (publishing) job that is currently active.

    Attributes:
        project_id: The project ID.
        connector_instance: The connector instance ID.
        timestamp: The starting time.
        progress: The total progress (0.0 - 1.0).
        message: The current activity message.
    """

    project_id: ProjectID
    connector_instance: ConnectorInstanceID

    timestamp: float

    progress: float
    message: str
