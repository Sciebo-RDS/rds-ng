from common.py.data.entities.project import ProjectExternalState

from ..osf import OSFProjectObject


def process_external_project_state(
    project: OSFProjectObject,
    external_state: ProjectExternalState,
) -> None:
    """
    Performs necessary logic for external project states.

    Args:
        project: The OSF project.
        external_state: The external project state to update.
    """
    # OSF doesn't lock projects
    external_state.external_state = ProjectExternalState.State.UPLOADED
