import { type ProjectFeatureID } from "../data/entities/EntityTypes";
import { ProjectFeature, ProjectFeatureFlags } from "./ProjectFeature";
import { type ProjectFeaturePanelLoader } from "./ProjectFeaturePanelLoader";

export class MetadataFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "metadata";

    public constructor(panel?: ProjectFeaturePanelLoader) {
        super(MetadataFeature.FeatureID, {
            flags: ProjectFeatureFlags.Optional,
            displayName: "Metadata",
            optionName: "Project metadata",
            panel: panel
        });
    }
}
