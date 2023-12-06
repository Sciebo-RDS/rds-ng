import { type ProjectFeatureID } from "../data/entities/EntityTypes";
import { ProjectFeature, ProjectFeatureFlags } from "./ProjectFeature";
import { type ProjectFeaturePanelLoader } from "./ProjectFeaturePanelLoader";

export class DataManagementPlanFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "dmp";

    public constructor(panel?: ProjectFeaturePanelLoader) {
        super(DataManagementPlanFeature.FeatureID, {
            flags: ProjectFeatureFlags.Optional,
            displayName: "Data Management Plan",
            optionName: "Data Management Plan",
            panel: panel
        });
    }
}
