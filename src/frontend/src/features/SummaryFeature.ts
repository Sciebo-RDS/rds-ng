import type { ProjectFeatureID } from "@common/data/entities/EntityTypes";
import { ProjectFeature, ProjectFeatureFlags } from "@common/features/ProjectFeature";

export class SummaryFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "summary";

    public constructor() {
        super(SummaryFeature.FeatureID, {
            flags: ProjectFeatureFlags.HasPanel,
            displayName: "Summary",
            panel: () => import("@/ui/content/features/SummaryPanel.vue")
        });
    }
}
