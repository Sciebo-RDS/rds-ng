import { WebComponent } from "../../../../component/WebComponent";
import { confirmDialog } from "../../../dialogs/ConfirmDialog";
import { PropertyObjectStore, SharedPropertyObject } from "../PropertyObjectStore";
import { type ProfileID, ProfileLayoutClass, PropertyProfile } from "../PropertyProfile";
import { PropertyProfileStore } from "../PropertyProfileStore";
import { injectTemplate } from "./Templates";

/**
 * Checks whether two profile IDs are the same.
 *
 * @param id1 - The first ProfileID.
 * @param id2 - The second ProfileID.
 * @returns - Whether the ProfileIDs are the same
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

/**
 * Builds a layout from a given PropertyProfileStore.
 *
 * @param projectProfiles The PropertyProfileStore that the layout is to be calculated for.
 * @returns the layout (profileLayoutClass[]).
 */
export function calculateLayout(projectProfiles: PropertyProfileStore): ProfileLayoutClass[] {
    const layout: ProfileLayoutClass[] = [];
    for (const profile of projectProfiles.list() as PropertyProfile[]) {
        for (const p of profile.getLayout()) {
            const x: ProfileLayoutClass | undefined = layout.find((xd: ProfileLayoutClass) => p.id == xd.id);
            if (x !== undefined) {
                x.addProfile(profile.getId());
                if (p.required) x["required"] = true;
            } else {
                p["profiles"] = [profile.getId()];
                layout.push(p);
            }
        }
    }
    return layout;
}

/**
 * Generates a list of linkable objects for a given parent ID and type.
 *
 * This function retrieves objects that are referenced in either the shared property object store
 * or the property object store, then filters out objects that are already linked or
 * have the same ID as the parent. It returns an array of objects with labels and commands
 * to add references to the property object stores.
 *
 * @param propertyObjects - The store containing property objects.
 * @param sharedPropertyObjectStore - The store containing shared property objects.
 * @param projectProfiles - The store containing property profiles.
 * @param parentId - The ID of the parent object.
 * @param type - The type of objects to link.
 * @returns An array of linkable objects with labels and commands.
 */
export function linkableObjects(
    propertyObjects: PropertyObjectStore,
    sharedPropertyObjectStore: PropertyObjectStore,
    projectProfiles: PropertyProfileStore,
    parentId: string,
    type: string
) {
    const linkedItems = [...sharedPropertyObjectStore.getReferencedObjects(parentId).flat(), ...propertyObjects.getReferencedObjects(parentId).flat()];
    const linkable = sharedPropertyObjectStore
        .getObjectsByType(type)
        .filter((item: SharedPropertyObject) => !linkedItems.includes(item.id))
        .filter((item: SharedPropertyObject) => item.id != parentId);
    return linkable.length > 0
        ? linkable.map((item: SharedPropertyObject) => ({
              label: injectTemplate(projectProfiles.getLabelTemplateById(item.type)!, sharedPropertyObjectStore.get(item.id)!),
              command: () => {
                  propertyObjects.addRef(parentId, item.id) || sharedPropertyObjectStore.addRef(parentId, item.id);
              }
          }))
        : [];
}

/**
 * Generates a list of actions for a linked item in a property editor.
 * Actions include unlinking the item and deleting the item.
 *
 * @param comp - The web component instance.
 * @param propertyObjects - The store containing property objects.
 * @param sharedPropertyObjectStore - The shared store containing property objects.
 * @param parentId - The ID of the parent object.
 * @param propertyObjectId - The ID of the property object.
 * @param classDisplayLabel - The label to display for the item.
 * @returns An array of action objects for the linked item.
 */
export function linkedItemActions(
    comp: WebComponent,
    propertyObjects: PropertyObjectStore,
    sharedPropertyObjectStore: PropertyObjectStore,
    parentId: string,
    propertyObjectId: string,
    classDisplayLabel: string
) {
    return [
        {
            label: `Remove ${classDisplayLabel}`,
            hasSubmenu: false,
            items: [
                {
                    label: `Unlink item`,
                    icon: "material-icons-outlined mi-link-off",
                    disabled: sharedPropertyObjectStore.get(propertyObjectId)!.isEmpty(),
                    command: () => {
                        confirmDialog(comp, {
                            header: `Unlink ${classDisplayLabel}?`,
                            message: "Are you sure you want to unlink this item? The object will not be deleted, you can relink at any time.",
                            acceptLabel: "Unlink",
                            acceptIcon: "pi pi-minus",
                            acceptClass: "p-button-danger",
                            rejectLabel: "Cancel",
                            rejectIcon: "pi pi-times",
                            rejectClass: "p-button-secondary"
                        }).then(() => {
                            propertyObjects.removeRef(parentId, propertyObjectId);
                            sharedPropertyObjectStore.removeRef(parentId, propertyObjectId);
                        });
                    }
                },
                { separator: true },
                {
                    label: "Delete item",
                    icon: "material-icons-outlined mi-delete-forever",
                    class: "r-text-error",
                    command: () => {
                        confirmDialog(comp, {
                            header: `Delete ${classDisplayLabel}?`,
                            message: "Are you sure you want to delete this item? It will not be recoverable.",
                            acceptLabel: "Delete",
                            acceptIcon: "pi pi-trash",
                            acceptClass: "p-button-danger",
                            rejectLabel: "Cancel",
                            rejectIcon: "pi pi-times",
                            rejectClass: "p-button-secondary"
                        }).then(() => {
                            propertyObjects.remove(propertyObjectId);
                            sharedPropertyObjectStore.remove(propertyObjectId);
                        });
                    }
                }
            ]
        }
    ];
}
