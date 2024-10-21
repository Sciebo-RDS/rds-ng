import { ProjectObject } from "../../../../ui/components/propertyeditor/ProjectObjectStore";
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
export class ProjectMetadataFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "project_metadata";

    public readonly metadata: ProjectMetadata;
    public readonly shared_objects: MetadataObjects;

    public constructor(metadata: ProjectMetadata = [], sharedObjects: MetadataObjects = []) {
        super();

        this.metadata = metadata;
        this.shared_objects = sharedObjects;
    }

    public get featureID(): ProjectFeatureID {
        return ProjectMetadataFeature.FeatureID;
    }
}
