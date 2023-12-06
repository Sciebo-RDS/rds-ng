from .project_feature import ProjectFeature


class DataManagementPlanFeature(ProjectFeature):
    FEATURE_ID = "dmp"

    def __init__(self):
        super().__init__(
            feature_id=DataManagementPlanFeature.FEATURE_ID,
            flags=ProjectFeature.FeatureFlags.OPTIONAL,
            display_name="Data Management Plan",
        )
