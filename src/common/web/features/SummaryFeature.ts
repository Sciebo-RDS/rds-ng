import { type ProjectFeatureID } from "../data/entities/EntityTypes";
import { ProjectFeature, ProjectFeatureFlags } from "./ProjectFeature";
import { type ProjectFeaturePanelLoader } from "./ProjectFeaturePanelLoader";

export class SummaryFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "summary";

    public constructor(panel?: ProjectFeaturePanelLoader) {
        super(SummaryFeature.FeatureID, {
            flags: ProjectFeatureFlags.None,
            displayName: "Summary",
            panel: panel
        });
    }
}
