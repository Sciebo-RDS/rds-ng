import typing
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .project_feature import ProjectFeature, ProjectFeatureID


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class MetadataFeature(ProjectFeature):
    """
    Data class for the metadata project feature.
    """

    feature_id: typing.ClassVar[ProjectFeatureID] = "metadata"
