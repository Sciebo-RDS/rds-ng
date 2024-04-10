import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .project_feature import ProjectFeature, ProjectFeatureID

ProjectMetadata = typing.List[typing.Dict[str, typing.Any]]  # TODO: Use proper type


@dataclass_json
@dataclass
class MetadataFeature(ProjectFeature):
    """
    Data class for the metadata project feature.
    """

    feature_id: typing.ClassVar[ProjectFeatureID] = "metadata"

    metadata: ProjectMetadata = field(default_factory=list)
