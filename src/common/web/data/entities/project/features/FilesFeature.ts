import { ProjectFeature, type ProjectFeatureID } from "./ProjectFeature";

/**
 * Data class for the files project feature.
 */
export class FilesFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "files";
}
