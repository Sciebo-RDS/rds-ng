import abc
import typing
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .. import ProjectFeatureID


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class ProjectFeature(abc.ABC):
    """
    Base data class for a project feature.
    """

    feature_id: typing.ClassVar[ProjectFeatureID]
