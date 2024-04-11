from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .data_management_plan_feature import DataManagementPlanFeature
from .metadata_feature import MetadataFeature
from .resources_metadata_feature import ResourcesMetadataFeature


@dataclass_json
@dataclass(kw_only=True)
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
