import typing

from .project_feature import ProjectFeature, ProjectFeatureID


class MetadataFeature(ProjectFeature):
    """
    Data class for the metadata project feature.
    """

    feature_id: typing.ClassVar[ProjectFeatureID] = "metadata"
