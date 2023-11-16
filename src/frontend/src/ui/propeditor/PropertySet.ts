import { SemVer } from "semver";
import { type PropertyProfile } from "./PropertyProfile";

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
    public readonly profile: PropertyProfile;
    public readonly properties: Property;
    public readonly profile_id: ProfileID;

    //FIXME profile ID hier doppelt gemoppelt, steht schon in den Properties
    public constructor(
        propertyProfile: PropertyProfile,
        propertyData: Property = { properties: {} as Property }
    ) {
        this.profile = propertyProfile;
        this.properties = propertyData["properties"] as Property;
        this.profile_id = [propertyProfile["name"], propertyProfile["version"]];
    }

    public setProperty(category: string, id: string, value: any): void {
        category in this.properties || (this.properties[category] = {});
        this.properties[category][id] = value;
    }

    public getProperty(category: string, id: string): any {
        return this.properties[category]?.[id];
    }

    public getProfile(): PropertyProfile {
        return this.profile;
    }

    public toString(): string {
        return JSON.stringify(this);
    }
}
