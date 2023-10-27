import { SemVer } from "semver";

export type ProfileID = [string, SemVer];
export type Property = {
    [category: string]: {
        [name: string]: any;
    };
};

/**
 * Data for a single **PropertySet**.
 *
 * @param profile_id - The tuple [name, version] that uniquely identifies the corresponding PropertyProfile.
 */
export class PropertySet {
    public readonly profile_id: ProfileID;
    public readonly properties: Property = {};

    public constructor(profileID: ProfileID) {
        this.profile_id = profileID;
    }

    public setProperty(category: string, name: string, value: any): void {
        this.properties[category] = { [name]: value };
    }
}
