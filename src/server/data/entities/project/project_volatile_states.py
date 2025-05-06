import threading
import time
import typing

from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.project import ProjectExternalState, ProjectID

from .project_volatile_state import ProjectVolatileState


class ProjectVolatileStates:
    """
    A map of all project volatile states (mapped using the project and connector instance ID).
    """

    STATE_LIFETIME = 60 * 60  # Keep states valid for one hour

    def __init__(self):
        self._states: typing.Dict[
            typing.Tuple[ProjectID, ConnectorInstanceID], ProjectVolatileState
        ] = {}

        self._lock = threading.RLock()

    def get(
        self, project_id: ProjectID, instance_id: ConnectorInstanceID
    ) -> ProjectVolatileState:
        """
        Gets the volatile state for a specific project and connector instance, creating a default one if necessary.

        Args:
            project_id: The project ID.
            instance_id: The connector instance ID.

        Returns:
            The volatile project state.
        """
        with self._lock:
            if not self.contains(project_id, instance_id):
                self._states[(project_id, instance_id)] = ProjectVolatileState(
                    project_id=project_id,
                    connector_instance=instance_id,
                    external_state=ProjectExternalState(
                        external_state=ProjectExternalState.State.UNKNOWN,
                        external_id="",
                    ),
                )
            return self._states[(project_id, instance_id)]

    def set(
        self,
        project_id: ProjectID,
        instance_id: ConnectorInstanceID,
        *,
        external_state: ProjectExternalState,
    ) -> None:
        """
        Sets the volatile state for a specific project and connector instance.

        Args:
            project_id: The project ID.
            instance_id: The connector instance ID.
            external_state: The project's external state.
        """
        with self._lock:
            state = self.get(project_id, instance_id)
            state.external_state = external_state
            state.timestamp = time.time()

    def contains(self, project_id: ProjectID, instance_id: ConnectorInstanceID) -> bool:
        """
        Checks whether a state is stored for a specific project and connector instance.

        Args:
            project_id: The project ID.
            instance_id: The connector instance ID.
        """
        with self._lock:
            return (project_id, instance_id) in self._states

    def get_states_by_project(
        self, project_id: ProjectID
    ) -> typing.Dict[
        typing.Tuple[ProjectID, ConnectorInstanceID], ProjectVolatileState
    ]:
        """
        Gets all states for a given project.

        Args:
            project_id: The project ID.
        """
        return {k: v for k, v in self._states.items() if v.project_id == project_id}

    def get_outdated_states(self) -> typing.List[ProjectVolatileState]:
        """
        Gets a list of all states that should be refreshed.
        """
        with self._lock:
            outdated_states = [
                state
                for state in self._states.values()
                if state.timestamp == 0
                or time.time() - state.timestamp >= self.STATE_LIFETIME
            ]
            for outdated_state in outdated_states:
                # Immediately update the state's timestamp to avoid floods of updates
                outdated_state.timestamp = time.time()
            return outdated_states
