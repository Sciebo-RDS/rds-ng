from dataclasses import dataclass

from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.project import ProjectExternalState, ProjectID


@dataclass(kw_only=True)
class ProjectVolatileState:
    """
    The volatile state of a project.

    Attributes:
        project_id: The project ID.
        connector_instance: The connector instaqnce ID.
        external_state: The project's external state.
        timestamp: The timestamp of the volatile state.
    """

    project_id: ProjectID
    connector_instance: ConnectorInstanceID

    external_state: ProjectExternalState

    timestamp: float = 0.0
