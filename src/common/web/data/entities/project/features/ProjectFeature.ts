import { Type } from "class-transformer";

import { type ProfileID } from "../../../../ui/components/propertyeditor/PropertyProfile";

/**
 * The project feature identifier type.
 */
export type ProjectFeatureID = string;

/**
 * Base data class for a project feature.
 */
export abstract class ProjectFeature {
    // @ts-ignore
    @Type(() => [String, String])
    public readonly enabled_metadata_profiles: ProfileID[] = [];

    /**
     * The ID of this feature.
     */
    public abstract get featureID(): ProjectFeatureID;

    public constructor(enabledProfiles: ProfileID[] = []) {
        this.enabled_metadata_profiles = enabledProfiles;
    }
}
