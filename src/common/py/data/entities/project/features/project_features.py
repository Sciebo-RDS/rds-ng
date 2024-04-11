import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .data_management_plan_feature import DataManagementPlanFeature
from .metadata_feature import MetadataFeature
from .project_feature import ProjectFeatureID, ProjectFeature
from .resources_metadata_feature import ResourcesMetadataFeature


@dataclass_json
@dataclass
class ProjectFeatures:
    """
    Superordinate data for all **Project** features.

    Attributes:
        metadata: The metadata project feature.
        resources_metadata: The resources metadata project feature.
        dmp: The data management plan feature.
    """

    project_id: int = 0  # TODO

    metadata: MetadataFeature = field(default_factory=MetadataFeature)
    resources_metadata: ResourcesMetadataFeature = field(
        default_factory=ResourcesMetadataFeature
    )
    dmp: DataManagementPlanFeature = field(default_factory=DataManagementPlanFeature)

    def features_dict(
        self, *, selected_features: typing.List[ProjectFeatureID] | None = None
    ) -> typing.Dict[ProjectFeatureID, ProjectFeature]:
        """
        Returns all or selected features as a dictionary (feature ID -> feature).

        Args:
            selected_features: Optional feature ID selection that should be returned.

        Returns:
            A dictonary containing the selected (or all) features.
        """
        features: typing.Dict[ProjectFeatureID, ProjectFeature] = {}

        def add_feature(feature_id: ProjectFeatureID, feature: ProjectFeature) -> None:
            if selected_features is None or feature_id in selected_features:
                features[feature_id] = feature

        # Important! When adding new features, always add them here as well
        add_feature(MetadataFeature.feature_id, self.metadata)
        add_feature(ResourcesMetadataFeature.feature_id, self.resources_metadata)
        add_feature(DataManagementPlanFeature.feature_id, self.dmp)

        return features
