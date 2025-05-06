import abc
from dataclasses import dataclass

from dataclasses_json import dataclass_json

ProjectFeatureID = str


@dataclass_json
@dataclass
class ProjectFeature(abc.ABC):
    """
    Base data class for a project feature.
    """
