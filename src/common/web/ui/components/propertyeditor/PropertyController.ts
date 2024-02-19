import logging from "@common/core/logging/Logging";

import { PropertySet, PersistedSet } from "./PropertySet";
import { type PropertyProfile, type PropertyCategory, type ProfileID } from "./PropertyProfile";

export abstract class PropertyController<S extends PropertySet | PropertySet[]> {
    defaultSet: PropertySet;
    mergeSets?: PropertySet[];
    propertySet?: PropertySet | PropertySet[];

    public constructor(defaultSet: PropertySet, mergeSets?: PropertySet[], propertySets?: S) {}

    public abstract getValue(profileId: ProfileID, category: string, id: string): any;
    public abstract setValue(profileId: ProfileID, debounce: number | null, category: string, id: string, value: any): number;
    public abstract getProfileIds(): ProfileID[];
    public abstract getProfile(id: ProfileID): PropertyProfile;
    public abstract getCategoryById(id: ProfileID): PropertyCategory[];
    public abstract exportData(): PersistedSet[];
    public abstract setsToWatch(): PropertySet[];
}

export class MetadataController extends PropertyController<PropertySet | PropertySet[]> {
    defaultSet: PropertySet;
    propertySets: PropertySet[];

    /**
     *
     * @param defaultSet - The default PropertySet (i.e. DataCite)
     * @param mergeSets - An array of PropertySet to be merged with the defaultSet (i.e. metadata required for a connector like OSF)
     * @param propertySet - One or more additinal PropertySets that will be displayed in an according (i.e. domain specific Metadata)
     */
    public constructor(defaultSet: PropertySet, mergeSets?: PropertySet[], propertySet?: PropertySet | PropertySet[]) {
        super(defaultSet, mergeSets, propertySet);
        if (!!propertySet) {
            if (Array.isArray(propertySet)) {
                this.propertySets = propertySet;
            } else {
                this.propertySets = [propertySet];
            }
        }

        if (mergeSets) {
            this.defaultSet = this.makeDefaultSet(defaultSet, mergeSets);
        } else {
            this.defaultSet = defaultSet;
        }
    }

    // FIXME Merge set properties are not covered
    public getValue(profileId: ProfileID, category: string, id: string): any {
        try {
            if (this.defaultSet?.profile_id === profileId) {
                return this.defaultSet?.getProperty(category, id);
            }
            return this._getPropertySet(profileId).getProperty(category, id);
        } catch (e: any) {
            logging.error(e, "PropertyController");
        }
    }

    public setValue(profileId: ProfileID, debounce: number | null, category: string, id: string, value: any): number {
        if (debounce) {
            clearTimeout(debounce);
        }

        return setTimeout(() => {
            try {
                if (this.defaultSet?.profile_id === profileId) {
                    this.defaultSet?.setProperty(category, id, value);
                }
                if (this._getPropertySet(profileId)) {
                    this._getPropertySet(profileId).setProperty(category, id, value);
                }
            } catch (e: any) {
                logging.error(e, "PropertyController");
            }
        }, 500);
    }

    public getProfileIds(): ProfileID[] {
        return this.propertySets.map((e) => e.profile_id);
    }

    public getProfile(id: ProfileID): PropertyProfile {
        return this._getPropertySet(id).profile;
    }

    public getCategoryById(id: ProfileID): PropertyCategory[] {
        return this._getPropertySet(id).profile.categories as PropertyCategory[];
    }

    private _getPropertySet(id: ProfileID): PropertySet {
        return this.propertySets.filter((e) => e.profile_id["name"] === id["name"] && e.profile_id["version"] === id["version"])[0];
    }

    public exportData(): PersistedSet[] {
        if (!this.defaultSet) {
            //is DMP
            return this.propertySets.map((e) => e.exportPropertySet());
        }
        const dS = this.defaultSet.exportPropertySet();
        const pS = this.propertySets.map((e) => e.exportPropertySet());

        return [dS, ...pS];
    }

    public makeDefaultSet(baseProfile: PropertySet, additionalProfiles: PropertySet[]): PropertySet {
        let dS = baseProfile;

        const defaultProperties = dS.getProperties();
        const additionalProperties = additionalProfiles.map((e) => e.getProperties())[0];

        for (const p of additionalProperties) {
            if (!defaultProperties.map((e) => e.id).includes(p.id)) {
                p.name = p.name + ` (${additionalProfiles[0].profile_id["name"]})`;
                dS.profile.categories[0].properties.push(p);
            }
        }

        return dS;
    }

    public getDefaultCategories(): PropertyCategory[] {
        return this.defaultSet?.profile.categories as PropertyCategory[];
    }

    public getDefaultProfile(): ProfileID {
        return this.defaultSet.profile_id;
    }

    public setsToWatch(): PropertySet[] {
        return [...this.propertySets, this.defaultSet];
    }
}

export class DmpController extends PropertyController<PropertySet | PropertySet[]> {
    dmpSet: PropertySet;

    public constructor(defaultSet: PropertySet) {
        super(defaultSet);

        this.dmpSet = defaultSet;
    }

    public getValue(profileId: ProfileID, category: string, id: string): any {
        try {
            return this._getPropertySet(profileId).getProperty(category, id);
        } catch (e) {
            // log failure
        }
    }

    public setValue(profileId: ProfileID, debounce: number | null, category: string, id: string, value: any): number {
        if (debounce) {
            clearTimeout(debounce);
        }

        return setTimeout(() => {
            try {
                this._getPropertySet(profileId).setProperty(category, id, value);
            } catch (e) {
                // log failure
            }
        }, 500);
    }

    public getProfileIds(): ProfileID[] {
        return [this.dmpSet.profile_id];
    }

    public getProfile(id: ProfileID): PropertyProfile {
        return this._getPropertySet(id).profile;
    }

    public getCategoryById(id: ProfileID): PropertyCategory[] {
        return this._getPropertySet(id).profile.categories as PropertyCategory[];
    }

    private _getPropertySet(id: ProfileID): PropertySet {
        if (this.dmpSet.profile_id === id) {
            return this.dmpSet;
        }
        // log failure
        return new PropertySet({} as PropertyProfile);
    }

    public exportData(): PersistedSet[] {
        return [this.dmpSet.exportPropertySet()];
    }

    public setsToWatch(): PropertySet[] {
        return [this.dmpSet];
    }
}
