import { type ProfileID } from "../PropertyProfile";

/**
 * Checks whether two profile IDs are the same.
 *
 * @param id1 - The first ID.
 * @param id2 - The second ID.
 */
export function compareProfileIDs(id1: ProfileID, id2: ProfileID): boolean {
    return id1[0].toLowerCase().localeCompare(id2[0].toLowerCase()) == 0 && id1[1].toLowerCase().localeCompare(id2[1].toLowerCase()) == 0;
}

/**
 * Retrieves a persisted set for a given profile ID from an array of persisted sets.
 *
 * @param persistedSets - The array of persisted sets.
 * @param profileID - The profile ID to extract.
 *
 * @returns - The found persisted set, if any.
 */
/* export function extractPersistedSetFromArray(persistedSets, profileID: ProfileID): PersistedSet {
    const sets = persistedSets.filter((set) => compareProfileIDs(set["metadata"]["id"], profileID));
    return sets.length ? sets[0] : ({} as PersistedSet);
} */

/**
 * Creates an intersection of a list of persisted sets.
 *
 * @param persistedSets - The sets to intersect.
 * @param profileID - The ID of the combined set.
 *
 * @returns - The combined set.
 */

/* export function intersectPersistedSets(persistedSets: PersistedSet[], profileID: ProfileID): PersistedSet {
    if (persistedSets.length == 0) {
        return new PersistedSet(profileID, {});
    } else if (persistedSets.length == 1) {
        return deepClone<PersistedSet>(persistedSets[0]);
    }

    let combinedSet = persistedSets[0];
    for (let i = 1; i < persistedSets.length; ++i) {
        combinedSet = intersectObjects(combinedSet, persistedSets[i]);
    }
    return new PersistedSet(profileID, combinedSet.categories || {});
} */

/**
 * Creates a debounced wrapper for arbitrary functions.
 *
 * @param waitFor The number of milliseconds to wait before invoking the wrapped function.
 * @returns A debounce wrapper.
 */
export function makeDebounce(waitFor: number = 1000) {
    let t: number;

    return <F extends (...args: any[]) => any>(func: F): Promise<ReturnType<F>> =>
        new Promise((resolve) => {
            if (t) {
                clearTimeout(t);
            }

            t = window.setTimeout(() => resolve(func()), waitFor);
        });
}
