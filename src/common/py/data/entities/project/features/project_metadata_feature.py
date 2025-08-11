import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from ...properties.properties_object import PropertyObject
from .project_feature import ProjectFeature, ProjectFeatureID

ProjectMetadata = typing.List[PropertyObject]


@dataclass_json
@dataclass
class ProjectMetadataFeature(ProjectFeature):
    """
    Data class for the project metadata project feature.
    """

    feature_id: typing.ClassVar[ProjectFeatureID] = "project_metadata"

    metadata: ProjectMetadata = field(default_factory=list)
