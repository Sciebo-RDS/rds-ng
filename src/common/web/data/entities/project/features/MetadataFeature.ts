import { ProjectFeature, type ProjectFeatureID } from "./ProjectFeature";

/**
 * Data class for the metadata project feature.
 */
export class MetadataFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "metadata";

    public get featureID(): ProjectFeatureID {
        return MetadataFeature.FeatureID;
    }
}
