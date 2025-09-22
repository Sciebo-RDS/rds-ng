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
    state = ProjectExternalState.State.UNKNOWN

    if (
        project.state == "inprogress" or project.state == "unsubmitted"
    ) and not project.is_submitted:
        state = ProjectExternalState.State.UPLOADED
    elif project.state == "done" or project.is_submitted:
        state = ProjectExternalState.State.LOCKED

    external_state.external_state = state
