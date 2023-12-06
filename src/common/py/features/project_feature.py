import abc
from enum import IntEnum

from ..data.entities import ProjectFeatureID


class ProjectFeature(abc.ABC):
    """
    A project feature containing meta information describing a single project feature.
    """

    class FeatureFlags(IntEnum):
        """
        Possible flags for a project feature.
        """

        NONE = 0

        OPTIONAL = 1 << 0

    def __init__(
        self, *, feature_id: ProjectFeatureID, flags: FeatureFlags, display_name: str
    ):
        self._feature_id = feature_id

        self._flags = flags

        self._display_name = display_name

    @property
    def feature_id(self) -> ProjectFeatureID:
        return self._feature_id

    def has_flags(self, flags: FeatureFlags) -> bool:
        return (self._flags & flags) == flags

    @property
    def display_name(self) -> str:
        return self._display_name
