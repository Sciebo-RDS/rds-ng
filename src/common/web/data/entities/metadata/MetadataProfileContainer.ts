import { PropertyProfile } from "../../../ui/components/propertyeditor/PropertyProfile";

/**
 * The role of a profile.
 */
export const enum MetadataProfileContainerRole {
    Template = "template",
    Global = "global"
}

/**
 * A container that holds a metadata profile along with various descriptive information.
 *
 * @param category - The overall category of the profile.
 * @param role - The role of the profile within its category.
 * @param profile - The actual profile data.
 */
export class MetadataProfileContainer {
    public readonly category: string;
    public readonly role: MetadataProfileContainerRole;

    public readonly profile: PropertyProfile;

    public constructor(category: string, role: MetadataProfileContainerRole, profile: PropertyProfile) {
        this.category = category;
        this.role = role;

        this.profile = profile;
    }
}

/**
 * A list of metadata profile containers.
 */
export type MetadataProfileContainerList = MetadataProfileContainer[];
