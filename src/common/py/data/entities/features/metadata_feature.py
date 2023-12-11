import typing

from .project_feature import SnapIn
from .. import ProjectFeatureID


class MetadataSnapIn(SnapIn):
    """
    Data class for the metadata project feature.
    """

    feature_id: typing.ClassVar[ProjectFeatureID] = "metadata"
