import abc
import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from ...properties import ProfileID

ProjectFeatureID = str


@dataclass_json
@dataclass
class ProjectFeature(abc.ABC):
    """
    Base data class for a project feature.
    """

    enabled_metadata_profiles: typing.List[ProfileID] = field(default_factory=list)
