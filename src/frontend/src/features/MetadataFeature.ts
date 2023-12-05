import type { ProjectFeatureID } from "@common/data/entities/EntityTypes";
import { ProjectFeature, ProjectFeatureFlags } from "@common/features/ProjectFeature";

export class MetadataFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "metadata";

    public constructor() {
        super(
            MetadataFeature.FeatureID,
            ProjectFeatureFlags.Optional,
            "Metadata",
            "Add metadata to the entire project"
        );
    }
}
