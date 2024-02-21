import logging from "../../../core/logging/Logging";

import { PropertySet, PersistedSet } from "./PropertySet";
import { type PropertyProfile, type PropertyCategory, type ProfileID } from "./PropertyProfile";

export type S = PropertySet | PropertySet[];

export abstract class PropertyController<S> {
    defaultSet!: PropertySet;

    public constructor(defaultSet: PropertySet) {}

    public abstract getValue(profileId: ProfileID, category: string, id: string): any;
    public abstract setValue(profileId: ProfileID, debounce: number | null, category: string, id: string, value: any): number;
    public abstract getProfileIds(): ProfileID[];
    public abstract getProfile(id: ProfileID): PropertyProfile;
    public abstract getCategoryById(id: ProfileID): PropertyCategory[];
    public abstract exportData(): PersistedSet[];
    public abstract setsToWatch(): PropertySet[];
}

export class MetadataController extends PropertyController<S> {
    mergeSets?: PropertySet[];
    propertySets?: PropertySet[];
    /**
     *
     * @param defaultSet - The default PropertySet (i.e. DataCite)
     * @param mergeSets - An array of PropertySet to be merged with the defaultSet (i.e. metadata required for a connector like OSF)
     * @param propertySet - One or more additinal PropertySets that will be displayed in an according (i.e. domain specific Metadata)
     */
    public constructor(defaultSet: PropertySet, mergeSets?: PropertySet[], propertySet?: S) {
        super(defaultSet);
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

        this._logLoadedSets(mergeSets);
    }

    public getValue(profileId: ProfileID, category: string, id: string): any {
        try {
            if (this.defaultSet.profile_id === profileId) {
                return this.defaultSet.getProperty(category, id);
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

        return window.setTimeout(() => {
            try {
                if (this.defaultSet.profile_id === profileId) {
                    this.defaultSet.setProperty(category, id, value);
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
        return this.propertySets?.map((e) => e.profile_id) || [];
    }

    public getProfile(id: ProfileID): PropertyProfile {
        return this._getPropertySet(id).profile;
    }

    public getCategoryById(id: ProfileID): PropertyCategory[] {
        return this._getPropertySet(id).profile.categories as PropertyCategory[];
    }

    private _getPropertySet(id: ProfileID): PropertySet {
        return this.propertySets!.filter((e) => e.profile_id["name"] === id["name"] && e.profile_id["version"] === id["version"])[0];
    }

    public exportData(): PersistedSet[] {
        const dS = this.defaultSet.exportPropertySet();
        const pS = this.propertySets?.map((e) => e.exportPropertySet());

        return [dS, ...(pS as PersistedSet[])];
    }

    public makeDefaultSet(baseProfile: PropertySet, additionalProfiles: PropertySet[]): PropertySet {
        const dS = baseProfile;
        const defaultProperties = dS.getProperties();

        for (const aP of additionalProfiles) {
            const properties = aP.getProperties();

            for (const p of properties) {
                if (!defaultProperties.filter((e) => e.id === p.id).length) {
                    p.name = p.name + ` (${aP.profile_id["name"]})`;
                    dS.profile.categories[0].properties.push(p);
                }
            }
        }

        return dS;
    }

    public getDefaultCategories(): PropertyCategory[] {
        return this.defaultSet.profile.categories as PropertyCategory[];
    }

    public getDefaultProfile(): ProfileID {
        return this.defaultSet.profile_id;
    }

    public setsToWatch(): PropertySet[] {
        return [...(this.propertySets as PropertySet[]), this.defaultSet];
    }

    private _logLoadedSets(mergeSets: PropertySet[] | null = null): void {
        if (!this.getDefaultProfile()) {
            logging.error(`Could not load a default profile.`, "MetadataEditor");
            return;
        }

        let log = `Loaded default profile ${JSON.stringify(this.getDefaultProfile())}${
            !!mergeSets ? ` with extension(s) ${mergeSets.map((e) => JSON.stringify(e.profile_id))}` : "without extensions"
        }.`;

        if (this.getProfileIds().length) {
            log += ` Loaded ${this.getProfileIds().length} additional profile(s): ${JSON.stringify(this.getProfileIds())}`;
        }

        logging.info(log, "MetadataEditor");
    }
}

export class DmpController extends PropertyController<S> {
    defaultSet: PropertySet;

    public constructor(defaultSet: PropertySet) {
        super(defaultSet);

        this.defaultSet = defaultSet;

        this._logLoadedSets();
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

        return window.setTimeout(() => {
            try {
                this._getPropertySet(profileId).setProperty(category, id, value);
            } catch (e) {
                // log failure
            }
        }, 500);
    }

    public getProfileIds(): ProfileID[] {
        return [this.defaultSet.profile_id];
    }

    public getProfile(id: ProfileID): PropertyProfile {
        return this._getPropertySet(id).profile;
    }

    public getCategoryById(id: ProfileID): PropertyCategory[] {
        return this._getPropertySet(id).profile.categories as PropertyCategory[];
    }

    private _getPropertySet(id: ProfileID): PropertySet {
        if (this.defaultSet.profile_id === id) {
            return this.defaultSet;
        }
        // log failure
        return new PropertySet({} as PropertyProfile);
    }

    public exportData(): PersistedSet[] {
        return [this.defaultSet.exportPropertySet()];
    }

    public setsToWatch(): PropertySet[] {
        return [this.defaultSet];
    }

    private _logLoadedSets(): void {
        if (!this.getProfileIds()) {
            logging.error(`Could not load a default profile.`, "DmpEditor");
            return;
        }

        logging.info(`Loaded DMP profile: ${JSON.stringify(this.getProfileIds())}`, "DmpEditor");
    }
}
