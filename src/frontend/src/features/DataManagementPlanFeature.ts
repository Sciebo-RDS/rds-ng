import type { ProjectFeatureID } from "@common/data/entities/EntityTypes";
import { ProjectFeature, ProjectFeatureFlags } from "@common/features/ProjectFeature";

export class DataManagementPlanFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "dmp";

    public constructor() {
        super(
            DataManagementPlanFeature.FeatureID,
            ProjectFeatureFlags.Optional,
            "Data Management Plan",
            "Write a Data Management Plan"
        );
    }
}
