import time
import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .project import ProjectID
from ..connector import ConnectorInstanceID
from ..user import UserID

ProjectJobID = typing.Tuple[ProjectID, ConnectorInstanceID]


@dataclass_json
@dataclass(kw_only=True)
class ProjectJob:
    """
    A project job that is currently active.

    Attributes:
        user_id: The ID of the user the job belongs to.
        project_id: The project ID.
        connector_instance: The connector instance ID.
        timestamp: The starting time.
        progress: The total progress (0.0 - 1.0).
        message: The current activity message.
    """

    user_id: UserID
    project_id: ProjectID
    connector_instance: ConnectorInstanceID

    timestamp: float = field(default_factory=lambda: time.time())

    progress: float = 0.0
    message: str = ""
