import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .project_feature import ProjectFeature, ProjectFeatureID

ResourcesMetadata = typing.List[typing.Dict[str, typing.Any]]  # TODO: Use proper type


@dataclass_json
@dataclass
class ResourcesMetadataFeature(ProjectFeature):
    """
    Data class for the resources metadata project feature.
    """

    feature_id: typing.ClassVar[ProjectFeatureID] = "resources_metadata"

    resources_metadata: ResourcesMetadata = field(default_factory=dict)
