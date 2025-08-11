import { Transform, Type, plainToInstance } from "class-transformer";

import { LayoutPropertyObject } from "../../../../ui/components/propertyeditor/PropertyObjectStore";
import { type ProfileID } from "../../../../ui/components/propertyeditor/PropertyProfile";
import { ProjectFeature, type ProjectFeatureID } from "./ProjectFeature";

/**
 * Represents the keys of the ResourcesMetadata object.
 */
export type ResourcesMetadataKey = keyof typeof ResourcesMetadata;

/**
 * The resources metadata type.
 *
 *
 */
export class ResourcesMetadata {
    [key: string]: LayoutPropertyObject;

    public constructor(metadata: { [key: string]: LayoutPropertyObject[] } = {}) {
        if (metadata.value === undefined) return;

        Object.entries(metadata.value).forEach(([key, value]: [string, LayoutPropertyObject]) => {
            if (value !== undefined) this[key as ResourcesMetadataKey] = plainToInstance(LayoutPropertyObject, value);
        });
    }
}

/**
 * Data class for the files project feature.
 */
export class ResourcesMetadataFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "resources_metadata";

    // @ts-ignore
    @Type(() => ResourcesMetadata)
    // @ts-ignore
    @Transform((value) => new ResourcesMetadata(value), { toClassOnly: false })
    public readonly metadata: ResourcesMetadata;

    public constructor(resourcesMetadata: ResourcesMetadata = {}, enabledProfiles: ProfileID[] = []) {
        super(enabledProfiles);

        this.metadata = resourcesMetadata;
    }

    public get featureID(): ProjectFeatureID {
        return ResourcesMetadataFeature.FeatureID;
    }
}
