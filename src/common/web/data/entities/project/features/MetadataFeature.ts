import { ProjectObject } from "@common/ui/components/propertyeditor/ProjectObjectStore";
import { ProjectFeature, type ProjectFeatureID } from "./ProjectFeature";

/**
 * The project metadata type.
 *
 * TODO: Use proper type
 */
export type ProjectMetadata = ProjectObject[];

/**
 * The metadata objects type.
 *
 * TODO: Use proper type
 */
export type MetadataObjects = ProjectObject[];

/**
 * Data class for the metadata project feature.
 */
export class MetadataFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "metadata";

    public readonly metadata: ProjectMetadata;
    public readonly shared_objects: MetadataObjects;

    public constructor(metadata: ProjectMetadata = [], sharedObjects: MetadataObjects = []) {
        super();

        this.metadata = metadata;
        this.shared_objects = sharedObjects;
    }

    public get featureID(): ProjectFeatureID {
        return MetadataFeature.FeatureID;
    }
}
