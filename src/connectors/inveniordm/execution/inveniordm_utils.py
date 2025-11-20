from common.py.data.entities.project import ProjectExternalState

from ..inveniordm import InvenioRDMProjectObject


def process_external_project_state(
    project: InvenioRDMProjectObject,
    external_state: ProjectExternalState,
) -> None:
    """
    Performs necessary logic for external project states.

    Args:
        project: The InvenioRDM project.
        external_state: The external project state to update.
    """
    state = ProjectExternalState.State.UPLOADED

    if project.is_published:
        state = ProjectExternalState.State.LOCKED

    external_state.external_state = state
