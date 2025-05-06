import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from ...properties.properties_object import PropertyObject
from .project_feature import ProjectFeature, ProjectFeatureID

DataManagementPlan = typing.List[PropertyObject]


@dataclass_json
@dataclass
class DataManagementPlanFeature(ProjectFeature):
    """
    Data class for the data management plan project feature.
    """

    feature_id: typing.ClassVar[ProjectFeatureID] = "dmp"

    plan: DataManagementPlan = field(default_factory=list)
