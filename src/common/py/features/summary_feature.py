from .project_feature import ProjectFeature


class SummaryFeature(ProjectFeature):
    FEATURE_ID = "summary"

    def __init__(self):
        super().__init__(
            feature_id=SummaryFeature.FEATURE_ID,
            flags=ProjectFeature.FeatureFlags.NONE,
            display_name="Summary",
        )
