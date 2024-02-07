import typing

from .project_feature import ProjectFeature, ProjectFeatureID


class ResourcesMetadataFeature(ProjectFeature):
    """
    Data class for the resources metadata project feature.
    """

    feature_id: typing.ClassVar[ProjectFeatureID] = "resources_metadata"
