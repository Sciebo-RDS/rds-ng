import typing

from .project_feature import ProjectFeature, ProjectFeatureID


class FilesFeature(ProjectFeature):
    """
    Data class for the files project feature.
    """

    feature_id: typing.ClassVar[ProjectFeatureID] = "files"
