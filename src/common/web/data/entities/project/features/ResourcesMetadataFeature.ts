import { ProjectObject } from "../../../../ui/components/propertyeditor/ProjectObjectStore";
import { ProjectFeature, type ProjectFeatureID } from "./ProjectFeature";

/**
 * The resources metadata type.
 *
 * TODO: Use proper type
 */
export type ResourcesMetadata = Record<string, ProjectObject[]>;

/**
 * Data class for the files project feature.
 */
export class ResourcesMetadataFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "resources_metadata";

    public readonly metadata: ResourcesMetadata;

    public constructor(resourcesMetadata: ResourcesMetadata = {}) {
        super();

        this.metadata = resourcesMetadata;
    }

    public get featureID(): ProjectFeatureID {
        return ResourcesMetadataFeature.FeatureID;
    }
}
