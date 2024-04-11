import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .project_feature import ProjectFeature, ProjectFeatureID

DataManagementPlan = typing.List[typing.Dict[str, typing.Any]]  # TODO: Use proper type


@dataclass_json
@dataclass(kw_only=True)
class DataManagementPlanFeature(ProjectFeature):
    """
    Data class for the data management plan project feature.
    """

    feature_id: typing.ClassVar[ProjectFeatureID] = "dmp"

    plan: DataManagementPlan = field(default_factory=list)
