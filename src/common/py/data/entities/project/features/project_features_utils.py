import typing

from .data_management_plan_feature import DataManagementPlanFeature
from .metadata_feature import MetadataFeature, ProjectFeatureID
from .project_features import ProjectFeatures
from .resources_metadata_feature import ResourcesMetadataFeature


def apply_project_features_update(
    features: ProjectFeatures,
    updated_features: ProjectFeatures,
    apply_to: typing.List[ProjectFeatureID] | None = None,
) -> None:
    """
    Applies updates to project features.

    Args:
        features: The features to apply the updates to.
        updated_features: The feature updates.
        apply_to: The features to update.
    """

    def apply_update(feature_id: ProjectFeatureID) -> None:
        if apply_to is None or feature_id in apply_to:
            setattr(features, feature_id, getattr(updated_features, feature_id))

    apply_update(MetadataFeature.feature_id)
    apply_update(ResourcesMetadataFeature.feature_id)
    apply_update(DataManagementPlanFeature.feature_id)
