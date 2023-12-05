import type { ProjectFeatureID } from "@common/data/entities/EntityTypes";
import { ProjectFeature, ProjectFeatureFlags } from "@common/features/ProjectFeature";

export class MetadataFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "metadata";

    public constructor() {
        super(MetadataFeature.FeatureID, {
            flags: ProjectFeatureFlags.Optional | ProjectFeatureFlags.HasPanel,
            displayName: "Metadata",
            optionName: "Project metadata",
            panel: () => import("@/ui/content/features/MetadataPanel.vue")
        });
    }
}
