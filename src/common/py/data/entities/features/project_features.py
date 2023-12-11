import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .data_management_plan_feature import DataManagementPlanSnapIn
from .metadata_feature import MetadataSnapIn
from .. import ProjectFeatureID


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class ProjectFeatures:
    """
    Superordinate data for all **Project** features.

    Attributes:
        metadata: The metadata project feature.
        dmp: The data management plan feature.
        optional_features: A list of all user-enabled optional features (this might include features that are only present in the UI bot not the backend).
    """

    metadata: MetadataSnapIn = field(default_factory=MetadataSnapIn)
    dmp: DataManagementPlanSnapIn = field(default_factory=DataManagementPlanSnapIn)

    optional_features: typing.List[ProjectFeatureID] = field(default_factory=list)
