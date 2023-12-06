from .project_feature import ProjectFeature


class MetadataFeature(ProjectFeature):
    FEATURE_ID = "metadata"

    def __init__(self):
        super().__init__(
            feature_id=MetadataFeature.FEATURE_ID,
            flags=ProjectFeature.FeatureFlags.OPTIONAL,
            display_name="Metadata",
        )
