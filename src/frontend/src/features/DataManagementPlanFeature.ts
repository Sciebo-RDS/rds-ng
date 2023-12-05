import type { ProjectFeatureID } from "@common/data/entities/EntityTypes";
import { ProjectFeature, ProjectFeatureFlags } from "@common/features/ProjectFeature";

export class DataManagementPlanFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "dmp";

    public constructor() {
        super(DataManagementPlanFeature.FeatureID, {
            flags: ProjectFeatureFlags.Optional | ProjectFeatureFlags.HasPanel,
            displayName: "Data Management Plan",
            optionName: "Data Management Plan",
            panel: () => import("@/ui/content/features/DataManagementPlanPanel.vue")
        });
    }
}
