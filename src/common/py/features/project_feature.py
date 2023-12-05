import abc
import dataclasses

from ..data.entities import ProjectFeatureID


@dataclasses.dataclass(frozen=True, kw_only=True)
class ProjectFeature(abc.ABC):
    """
    A project feature containing meta information describing a single project feature.

    Attributes:
        feature_id: The project feature ID.
    """

    feature_id: ProjectFeatureID
