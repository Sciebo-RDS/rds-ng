import logging from "../../../core/logging/Logging";

import { PropertySet, PersistedSet } from "./PropertySet";
import { type PropertyProfile, type PropertyCategory, type ProfileID } from "./PropertyProfile";
import { type Property, type SelectionProperty } from "./PropertyProfile";
import { compareProfileIDs } from "./utils/PropertyEditorUtils";

export type S = PropertySet | PropertySet[];

export abstract class PropertyController<S> {
    propertySets?: PropertySet[];
    public constructor(public defaultSet: PropertySet) {}

    /**
     * Retrieves the value of a property based on the profile ID, category, and ID.
     *
     * @param profileId - The ID of the profile.
     * @param category - The category of the property.
     * @param id - The ID of the property.
     * @returns The value of the property.
     */
    public getValue(profileId: ProfileID, category: string, id: string): any {
        try {
            return this._getPropertySet(profileId).properties[category]?.[id];
        } catch (e: any) {
            logging.error(e, "PropertyController");
        }
    }

    /**
     * Sets the value of a property.
     *
     * @param profileId - The profile ID.
     * @param debounce - The debounce time in milliseconds. Set to null for no debounce.
     * @param category - The category of the property.
     * @param id - The ID of the property.
     * @param value - The new value of the property.
     * @returns The timeout ID.
     */
    public setValue(profileId: ProfileID, category: string, id: string, value: any): void {
        try {
            const pS = this._getPropertySet(profileId);
            category in pS.properties || (pS.properties[category] = {});
            pS.properties[category][id] = value;
        } catch (e: any) {
            logging.error(e, "PropertyController");
        }
    }

    /**
     * Retrieves the property categories by their ID.
     *
     * @param id - The ID of the profile.
     * @returns An array of property categories.
     */
    public getCategoryById(id: ProfileID): PropertyCategory[] {
        return this._getPropertySet(id).profile.categories as PropertyCategory[];
    }

    /**
     * Retrieves the property profile for the specified ID.
     * @param id The ID of the profile to retrieve.
     * @returns The property profile associated with the ID.
     */
    public getProfile(id: ProfileID): PropertyProfile {
        return this._getPropertySet(id).profile;
    }

    /**
     * Exports the data from the PropertyController.
     * @returns An array of PersistedSet objects.
     */
    public exportData(): PersistedSet[] {
        return [this.defaultSet, ...(this.propertySets || [])].map((e) => new PersistedSet(e.profile_id, e.properties));
    }

    abstract _getPropertySet(profileId: ProfileID): PropertySet;
    abstract getProfileIds(): ProfileID[];
    abstract mountPersistedSets(persistedSets: PersistedSet[]): void;
}

/**
 * Represents a controller for managing metadata properties.
 * @template S - The type of additional property sets.
 */
export class MetadataController extends PropertyController<S> {
    /**
     * Constructs a new instance of the PropertyController class.
     * @param defaultSet The default property set.
     * @param mergeSets Optional. An array of property sets to merge with the default set.
     * @param propertySet Optional. A single property set or an array of property sets.
     */
    public constructor(defaultSet: PropertySet, mergeSets: PropertySet[] = [], propertySet?: S) {
        super(defaultSet);
        if (!!propertySet) {
            if (Array.isArray(propertySet)) {
                this.propertySets = propertySet;
            } else {
                this.propertySets = [propertySet];
            }
        }

        this.defaultSet = this.makeDefaultSet(defaultSet, mergeSets);

        this._logLoadedSets(mergeSets);
    }

    /**
     * Mounts the persisted sets onto the property controller.
     *
     * @param persistedSets - The persisted sets to be mounted.
     */
    public mountPersistedSets(persistedSets: any): void {
        for (const pS of [this.defaultSet, ...(this.propertySets || [])]) {
            const s = persistedSets.filter((e: PersistedSet) => compareProfileIDs(e.profile_id, pS.profile_id));
            if (!s.length) {
                const newSet: PersistedSet = new PersistedSet(pS.profile_id);
                pS.properties = newSet["categories"];
                persistedSets.push(newSet);
            } else {
                pS.properties = s[0]["categories"];
            }
        }
    }

    /**
     * Retrieves the value of a property based on the given profile ID, category, and ID.
     * If the profile ID matches the default set, the value is retrieved from the default set.
     * Otherwise, the value is retrieved from the property set associated with the given profile ID.
     * @param profileId - The ID of the profile.
     * @param category - The category of the property.
     * @param id - The ID of the property.
     * @returns The value of the property.
     */

    /**
     * Retrieves an array of ProfileIDs from the propertySets.
     * @returns {ProfileID[]} An array of ProfileIDs.
     */
    public getProfileIds(): ProfileID[] {
        return this.propertySets?.map((e) => e.profile_id) || ([] as ProfileID[]);
    }

    private getProfileProperties(profile: PropertyProfile): (Property | SelectionProperty)[] {
        return profile.categories.map((categories) => categories.properties).flat();
    }

    _getPropertySet(id: ProfileID): PropertySet {
        return [this.defaultSet, ...this.propertySets!].filter((e) => compareProfileIDs(e.profile_id, id))[0] || ({} as PropertySet);
    }

    /**
     * Creates a default property set by combining a base profile with additional profiles.
     * @param baseProfile - The base profile to start with.
     * @param additionalProfiles - An array of additional profiles to merge with the base profile.
     * @returns The resulting property set.
     */
    public makeDefaultSet(baseProfile: PropertySet, additionalProfiles: PropertySet[]): PropertySet {
        const dS = baseProfile;
        const defaultProperties = this.getProfileProperties(dS.profile);

        for (const aP of additionalProfiles) {
            const properties = this.getProfileProperties(aP.profile);

            for (const p of properties) {
                if (!defaultProperties.filter((e) => e.id === p.id).length) {
                    p.name = p.name + ` (${aP.profile_id["name"]})`;
                    dS.profile.categories[0].properties.push(p);
                }
            }
        }

        return dS;
    }

    /**
     * Retrieves the default categories for the property controller.
     *
     * @returns An array of PropertyCategory objects representing the default categories.
     */
    public getDefaultCategories(): PropertyCategory[] {
        return this.defaultSet.profile.categories as PropertyCategory[];
    }

    /**
     * Retrieves the default profile ID.
     *
     * @returns The default profile ID.
     */
    public getDefaultProfile(): ProfileID {
        return this.defaultSet.profile_id;
    }

    private _logLoadedSets(mergeSets: PropertySet[] | null = null): void {
        if (!this.getDefaultProfile()) {
            logging.error(`Could not load a default profile.`, typeof self);
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

/**
 * Represents a controller for managing properties in a property editor.
 * @template S - The type of the property set.
 */
export class DmpController extends PropertyController<S> {
    /**
     * Creates a new instance of the DmpController class.
     * @param defaultSet - The default property set.
     */
    public constructor(defaultSet: PropertySet) {
        super(defaultSet);

        this._logLoadedSets();
    }

    /**
     * Mounts the persisted sets onto the property controller.
     * @param persistedSets[] - The persisted set(s) to mount.
     */
    public mountPersistedSets(persistedSets: PersistedSet[]): void {
        const persistedSet: PersistedSet = persistedSets.filter(
            (e: PersistedSet) => Object.keys(e).includes("profile_id") && compareProfileIDs(e.profile_id, this.defaultSet.profile_id)
        )[0];
        if (!!persistedSet) {
            this.defaultSet.properties = persistedSet["categories"];
        } else {
            const newSet: PersistedSet = new PersistedSet(this.defaultSet.profile_id);
            this.defaultSet.properties = newSet["categories"];
            persistedSets = [newSet];
        }
    }

    /**
     * Gets the profile IDs.
     * @returns An array of profile IDs.
     */
    public getProfileIds(): ProfileID[] {
        return [this.defaultSet.profile_id];
    }

    /**
     * Gets the property set for a given profile ID.
     * @param id - The profile ID.
     * @returns The property set.
     */
    _getPropertySet(id: ProfileID): PropertySet {
        return compareProfileIDs(this.defaultSet.profile_id, id) ? this.defaultSet : new PropertySet({} as PropertyProfile);
    }

    /**
     * Logs the loaded sets.
     */
    private _logLoadedSets(): void {
        if (!this.getProfileIds()) {
            logging.error(`Could not load a default profile.`, typeof this);
            return;
        }

        logging.info(`Loaded DMP profile: ${JSON.stringify(this.getProfileIds())}`, "DmpEditor");
    }
}
