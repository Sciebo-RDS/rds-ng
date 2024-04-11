import typing

from .features import ProjectFeatureID
from .project import Project, ProjectID


def find_project_by_id(
    projects: typing.List[Project], project_id: ProjectID
) -> Project | None:
    """
    Searches for a project by its ID within a list of projects.

    Args:
        projects: The list of projects.
        project_id: The project to search for.

    Returns:
        The found project or **None** otherwise.
    """
    matching_project = (proj for proj in projects if proj.project_id == project_id)
    return next(matching_project, None)


def apply_project_features_update(
    project: Project,
    updated_features: Project.Features,
    apply_to: typing.List[ProjectFeatureID] | None = None,
) -> None:
    """
    Applies updates to project features.

    Args:
        project: The project to apply the updates to.
        updated_features: The feature updates.
        apply_to: The features to update.
    """

    def apply_update(feature_id: ProjectFeatureID) -> None:
        if apply_to is None or feature_id in apply_to:
            setattr(project.features, feature_id, getattr(updated_features, feature_id))

    from common.py.data.entities.project.features import (
        MetadataFeature,
        ResourcesMetadataFeature,
        DataManagementPlanFeature,
    )

    apply_update(MetadataFeature.feature_id)
    apply_update(ResourcesMetadataFeature.feature_id)
    apply_update(DataManagementPlanFeature.feature_id)
