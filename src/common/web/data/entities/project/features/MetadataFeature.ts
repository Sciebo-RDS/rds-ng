import { ProjectFeature, type ProjectFeatureID } from "./ProjectFeature";

/**
 * The project metadata type.
 *
 * TODO: Use proper type
 */
export type ProjectMetadata = Record<string, any>[];

/**
 * Data class for the metadata project feature.
 */
export class MetadataFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "metadata";

    public readonly metadata: ProjectMetadata;

    public constructor(metadata: ProjectMetadata = []) {
        super();

        this.metadata = metadata;
    }

    public get featureID(): ProjectFeatureID {
        return MetadataFeature.FeatureID;
    }
}
