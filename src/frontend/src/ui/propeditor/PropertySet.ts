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
    public readonly properties: Property;

    //FIXME profile ID hier doppelt gemoppelt, steht schon in den Properties
    public constructor(
        profile_id: ProfileID,
        propertyData: Property = { properties: {} as Property }
    ) {
        this.properties = propertyData["properties"] as Property;
    }

    public setProperty(category: string, id: string, value: any): void {
        category in this.properties || (this.properties[category] = {});
        this.properties[category][id] = value;
    }

    public getProperty(category: string, id: string): any {
        return this.properties[category]?.[id];
    }

    public toString(): string {
        return JSON.stringify(this);
    }
}
