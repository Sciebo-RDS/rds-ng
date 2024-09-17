import { ProjectObject } from "@common/ui/components/propertyeditor/ProjectObjectStore";
import { ProjectFeature, type ProjectFeatureID } from "./ProjectFeature";

/**
 * The resources metadata type.
 *
 * TODO: Use proper type
 */
export type ResourcesMetadata = ProjectObject[];

/**
 * Data class for the files project feature.
 */
export class ResourcesMetadataFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "resources_metadata";

    public readonly resources_metadata: ResourcesMetadata;

    public constructor(resourcesMetadata: ResourcesMetadata = []) {
        super();

        this.resources_metadata = resourcesMetadata;
    }


    public get featureID(): ProjectFeatureID {
        return ResourcesMetadataFeature.FeatureID;
    }
}
