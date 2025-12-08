from common.py.data.entities.project import ProjectExternalState

from ..dataverse import DataverseDatasetObject


def process_external_project_state(
    project: DataverseDatasetObject,
    external_state: ProjectExternalState,
) -> None:
    """
    Performs necessary logic for external project states.

    Args:
        project: The Dataverse project.
        external_state: The external project state to update.
    """
    # Dataverse doesn't lock projects
    # TODO: o rly?
    external_state.external_state = ProjectExternalState.State.UPLOADED
