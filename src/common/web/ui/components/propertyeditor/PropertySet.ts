import { deepClone } from "@common/utils/ObjectUtils";
import { type Profile, type ProfileID } from "./PropertyProfile";
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
 * @param profileId - The ProfileID that uniquely identifies the corresponding Profile.

 */
export class PropertySet {
    public properties: Properties = {} as Properties;
    public readonly profile_id: ProfileID;

    public constructor(public profile: Profile) {
        this.profile = deepClone(profile);

        if (!this._validateProfile()) {
            throw new Error("PropertyProfile does not have a valid ProfileID.");
        }

        this.profile_id = profile["profile_id"];
    }

    private _validateProfile() {
        return this.profile["profile_id"]?.["name"] && this.profile["profile_id"]?.["version"];
    }
}
