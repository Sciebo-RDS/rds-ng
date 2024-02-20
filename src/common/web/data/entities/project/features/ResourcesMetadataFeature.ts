import { ProjectFeature, type ProjectFeatureID } from "./ProjectFeature";

/**
 * Data class for the files project feature.
 */
export class ResourcesMetadataFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "resources_metadata";

    public get featureID(): ProjectFeatureID {
        return ResourcesMetadataFeature.FeatureID;
    }
}
