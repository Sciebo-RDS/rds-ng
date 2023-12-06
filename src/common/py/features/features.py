import typing

from .data_management_plan_feature import DataManagementPlanFeature
from .metadata_feature import MetadataFeature
from .project_features_catalog import ProjectFeaturesCatalog
from .summary_feature import SummaryFeature
from ..core.logging import debug


def register_project_features() -> None:
    """
    Registers all available project features.

    When adding a new project feature, always register it here.
    """

    def register_feature(feat) -> None:
        ProjectFeaturesCatalog.register_item(feat.FEATURE_ID, feat())

    #  New project features go here
    register_feature(MetadataFeature)
    register_feature(DataManagementPlanFeature)
    register_feature(SummaryFeature)

    # Print all available features for debugging purposes
    names: typing.List[str] = []
    for feature_id, feature in ProjectFeaturesCatalog.items():
        names.append(f"{feature.display_name} ({feature_id})")
    debug(f"Registered project features: {'; '.join(names)}")
