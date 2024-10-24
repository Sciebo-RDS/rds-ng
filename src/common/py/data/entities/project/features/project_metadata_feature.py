import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .project_feature import ProjectFeature, ProjectFeatureID

ProjectMetadata = typing.List[typing.Dict[str, typing.Any]]  # TODO: Use proper type
MetadataObjects = typing.List[typing.Dict[str, typing.Any]]  # TODO: Use proper type


@dataclass_json
@dataclass
class ProjectMetadataFeature(ProjectFeature):
    """
    Data class for the project metadata project feature.
    """

    feature_id: typing.ClassVar[ProjectFeatureID] = "project_metadata"

    metadata: ProjectMetadata = field(default_factory=list)
    shared_objects: MetadataObjects = field(default_factory=list)
