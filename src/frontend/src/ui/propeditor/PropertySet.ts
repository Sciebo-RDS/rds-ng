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
 * @param profileId - The tuple [name, version] that uniquely identifies the corresponding PropertyProfile.
 * @param properties - Property data values

*/
export class PropertySet {
    public readonly profile_id: ProfileID;
    public readonly properties: Property = {};

    public constructor(profileID: ProfileID, properties: Property = {}) {
        this.profile_id = profileID;
        this.properties = properties["properties"];
    }

    public setProperty(category: string, name: string, value: any): void {
        this.properties[category][name] = value;
    }

    public getProperty(category: string, name: string): any {
        return this.properties[category][name];
    }
}
