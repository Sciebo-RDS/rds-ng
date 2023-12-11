import { type ProjectFeatureID } from "../EntityTypes";
import { ProjectFeature } from "./ProjectFeature";

/**
 * Data class for the metadata project feature.
 */
export class MetadataFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "metadata";
}
