import typing

from .project_feature import SnapIn
from .. import ProjectFeatureID


class DataManagementPlanSnapIn(SnapIn):
    """
    Data class for the data management plan project feature.
    """

    feature_id: typing.ClassVar[ProjectFeatureID] = "dmp"
