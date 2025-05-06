from common.py.data.entities.project import ProjectExternalState


def process_external_project_state(
    external_state: ProjectExternalState,
) -> None:
    """
    Performs necessary logic for external project states.

    Args:
        external_state: The external project state to update.
    """
    external_state.external_state = ProjectExternalState.State.DEFAULT
