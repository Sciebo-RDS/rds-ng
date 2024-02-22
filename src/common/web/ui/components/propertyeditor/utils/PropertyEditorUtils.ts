import { type ProfileID } from "../PropertyProfile";
import { PersistedSet, Properties } from "../PropertySet";

/**
 * Checks whether two profile IDs are the same.
 *
 * @param id1 - The first ID.
 * @param id2 - The second ID.
 */
export function compareProfileIDs(id1: ProfileID, id2: ProfileID): boolean {
    return id1.name.toLowerCase().localeCompare(id2.name.toLowerCase()) == 0 && id1.version.toLowerCase().localeCompare(id2.version.toLowerCase()) == 0;
}

/**
 * Retrieves a persisted set for a given profile ID from an array of persisted sets.
 *
 * @param persistedSets - The array of persisted sets.
 * @param profileID - The profile ID to extract.
 *
 * @returns - The found persisted set, if any.
 */
export function extractPersistedSetFromArray(persistedSets: PersistedSet[], profileID: ProfileID): PersistedSet {
    const sets = persistedSets.filter((set) => compareProfileIDs(set.profile_id, profileID));
    return sets.length ? sets[0] : {} as PersistedSet;
}

/**
 * Creates an intersection of a list of persisted sets.
 *
 * @param persistedSets - The sets to intersect.
 *
 * @returns - The combined set.
 */
export function intersectPersistedSets(persistedSets: PersistedSet[]): PersistedSet {
    let profileID: ProfileID = { name: "UnifiedSet", version: "0.0.0" };
    let properties: Properties = {};

    // Category -> Property
    for (const persistedSet of persistedSets) {
        const keys = new Set(Object.keys(persistedSet.categories));
    }
}
