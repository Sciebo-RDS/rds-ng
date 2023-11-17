import { PropertySet, type PersistedPropertySet } from "./PropertySet";
import {
    type PropertyProfile,
    type PropertyCategory,
    type ProfileID,
} from "./PropertyProfile";

export interface PropertyController {
    propertySets: PropertySet[];

    getValue(profileId: ProfileID, category: string, id: string): any;
    setValue(
        profileId: ProfileID,
        debounce: number | null,
        category: string,
        id: string,
        value: any
    ): void;
    getProfileIds(): ProfileID[];
    getProfile(id: ProfileID): PropertyProfile;
    getCategoryById(id: ProfileID): PropertyCategory[];
    exportData(): PersistedPropertySet[];
}

export class MetadataController implements PropertyController {
    propertySets: PropertySet[];

    public constructor(propertySet: PropertySet | PropertySet[]) {
        if (Array.isArray(propertySet)) {
            this.propertySets = propertySet;
        } else {
            this.propertySets = [propertySet];
        }
    }

    public getValue(profileId: ProfileID, category: string, id: string): any {
        return this.getPropertySet(profileId).getProperty(category, id);
    }

    public setValue(
        profileId: ProfileID,
        debounce: number | null,
        category: string,
        id: string,
        value: any
    ): number {
        if (debounce) {
            clearTimeout(debounce);
        }

        return setTimeout(() => {
            this.getPropertySet(profileId).setProperty(category, id, value);
        }, 500);
    }

    public getProfileIds(): ProfileID[] {
        return this.propertySets.map((e) => e.profile_id);
    }

    public getProfile(id: ProfileID): PropertyProfile {
        return this.getPropertySet(id).profile;
    }

    public getCategoryById(id: ProfileID): PropertyCategory[] {
        return this.getPropertySet(id).profile.categories as PropertyCategory[];
    }

    private getPropertySet(id: ProfileID): PropertySet {
        return this.propertySets.filter(
            (e) =>
                e.profile_id["name"] === id["name"] &&
                e.profile_id["version"] === id["version"]
        )[0];
    }

    public exportData(): PersistedPropertySet[] {
        return this.propertySets.map((e) => e.exportPropertySet());
    }
}
