import { deepClone } from "@common/utils/ObjectUtils";
import { type PropertyProfile, type ProfileID } from "./PropertyProfile";
import { compareProfileIDs } from "./utils/PropertyEditorUtils";

export type Properties = {
    [category: string]: {
        [id: string]: any;
    };
};

export class PersistedSet {
    public profile_id: ProfileID;
    public categories: Properties;

    public constructor(profile_id: ProfileID, categories: Properties = {} as Properties) {
        this.profile_id = profile_id;
        this.categories = categories;
    }
}

/**
 * Data for a single **PropertySet**.
 *
 * @param profileId - The ProfileID that uniquely identifies the corresponding PropertyProfile.
 * @param properties - Property data values

 */
export class PropertySet {
    public properties: Properties;
    public readonly profile_id: ProfileID;

    public constructor(
        public profile: PropertyProfile,
        propertyData: PersistedSet = {} as PersistedSet
    ) {
        this.profile = deepClone(profile);

        if (!this._validateProfile()) {
            throw new Error("PropertyProfile is not valid.");
        }

        this.profile_id = profile["profile_id"];

        if (Object.keys(propertyData).includes("profile_id")) {
            if (!this._dataMatchesProfile(propertyData["profile_id"], profile["profile_id"])) {
                throw new Error(
                    `Provided data does not match profile. Data uses profile \"${propertyData["profile_id"]["name"]} ${propertyData["profile_id"]["version"]}\" but profile is \"${profile["profile_id"]["name"]} ${profile["profile_id"]["version"]}\".`
                );
            }

            this.properties = propertyData["categories"] as Properties;
        } else {
            this.properties = {} as Properties;
        }
    }

    private _validateProfile() {
        return this.profile["profile_id"]?.["name"] && this.profile["profile_id"]?.["version"];
    }

    private _dataMatchesProfile(propertyDataId: ProfileID, profileProfileId: ProfileID) {
        return compareProfileIDs(propertyDataId, profileProfileId);
    }
}
