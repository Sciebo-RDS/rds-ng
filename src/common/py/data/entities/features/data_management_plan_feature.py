import typing

from .project_feature import ProjectFeature, ProjectFeatureID


class DataManagementPlanFeature(ProjectFeature):
    """
    Data class for the data management plan project feature.
    """

    feature_id: typing.ClassVar[ProjectFeatureID] = "dmp"
