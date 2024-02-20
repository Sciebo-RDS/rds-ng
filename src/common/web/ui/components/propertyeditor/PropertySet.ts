import { type PropertyProfile, type ProfileID } from "./PropertyProfile";

export type Properties = {
    [category: string]: {
        [id: string]: any;
    };
};

export class PersistedSet {
    public readonly profile_id: ProfileID;
    public readonly categories: Properties;

    public constructor(profile_id: ProfileID, categories: Properties) {
        this.profile_id = profile_id;
        this.categories = categories;
    }
}

/**
 * Data for a single **PropertySet**.
 *
 * @param profileId - The ID {name: string, version: string} that uniquely identifies the corresponding PropertyProfile.
 * @param properties - Property data values

*/
export class PropertySet {
    public readonly properties: Properties;
    public readonly profile_id: ProfileID;

    public constructor(
        public profile: PropertyProfile,
        public propertyData: PersistedSet = {} as PersistedSet,
    ) {
        if (!this._validateProfile()) {
            throw new Error("PropertyProfile is not valid.");
        }

        this.profile_id = profile["profile_id"];

        if (!("profile_id" in Object.keys(propertyData))) {
            this.properties = {} as Properties;
            return;
        }

        if (!this._dataMatchesProfile(propertyData["profile_id"], profile["profile_id"])) {
            throw new Error(
                `Provided data does not match profile. Data uses profile \"${propertyData["profile_id"]["name"]} ${propertyData["profile_id"]["version"]}\" but profile is \"${profile["profile_id"]["name"]} ${profile["profile_id"]["version"]}\".`,
            );
        }

        this.properties = propertyData["categories"] as Properties;
    }

    public setProperty(category: string, id: string, value: any): void {
        category in this.properties || (this.properties[category] = {});
        this.properties[category][id] = value;
    }

    public getProperty(category: string, id: string): Properties {
        return this.properties[category]?.[id];
    }

    public getProperties() {
        let p = [];
        for (const category of this.profile.categories) {
            for (const property of category.properties) {
                p.push(property);
            }
        }
        return p;
    }

    public getProfile(): PropertyProfile {
        return this.profile;
    }

    public toString(): string {
        return JSON.stringify(this);
    }

    public exportPropertySet() {
        return new PersistedSet(this.profile_id, this.properties);
    }

    private _validateProfile() {
        return this.profile["profile_id"]?.["name"] && this.profile["profile_id"]?.["version"];
    }

    private _dataMatchesProfile(propertyDataId: ProfileID, profileProfileId: ProfileID) {
        return propertyDataId["name"] === profileProfileId["name"] && propertyDataId["version"] === profileProfileId["version"];
    }
}
