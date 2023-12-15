import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .data_management_plan_feature import DataManagementPlanFeature
from .metadata_feature import MetadataFeature
from .project_feature import ProjectFeatureID, ProjectFeature


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class ProjectFeatures:
    """
    Superordinate data for all **Project** features.

    Attributes:
        metadata: The metadata project feature.
        dmp: The data management plan feature.
    """

    metadata: MetadataFeature = field(default_factory=MetadataFeature)
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
        add_feature(DataManagementPlanFeature.feature_id, self.dmp)

        return features
