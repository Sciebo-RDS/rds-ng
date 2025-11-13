import { Resource, ResourceType } from "@common/data/entities/resource/Resource.ts";
import { ResourcesList } from "@common/data/entities/resource/ResourcesList.ts";
import { resourcesListFindPath, resourcesListRemovePath } from "@common/data/entities/resource/ResourceUtils.ts";

/**
 * A single resources list entry in the resources lists cache.
 */
class ResourcesListCacheEntry {
    private readonly _root: string;

    private _resourcesList: ResourcesList | null = null;
    private _knownPaths: string[] = [];

    public constructor(root: string) {
        this._root = root;
    }

    /**
     * Adds a new resources list to the cache.
     *
     * The new list must be either located under the root path or a new root path. Errors will be thrown if a push would potentially result in a corrupted
     * cache (i.e., when adding an already existing path, or gaps would occur).
     *
     * @param resources - The new resources list to add.
     *
     * @throws Error - When a push operation would result in a corrupted cache.
     */
    public push(resources: ResourcesList): void {
        // Adding a new root replaces everything else
        if (this.isRoot(resources.resource)) {
            this.clear();

            this._resourcesList = resources;
        } else {
            if (this.isEmpty()) {
                throw new Error(`Tried to push a non-root resources list (${resources.resource.filename}) into an empty cache`);
            } else if (this.contains(resources.resource.filename)) {
                throw new Error(`Tried to push an already existing resources list (${resources.resource.filename})`);
            }

            if (!this.insertIntoParent(this._resourcesList!, resources)) {
                throw new Error(`Unable to push the resources list (${resources.resource.filename}) into the cache`);
            }
        }

        this._knownPaths.push(resources.resource.filename);
        this.updateResourceSizes();
    }

    /**
     * Gets the resources list of a specific path.
     *
     * @param path - The path to get.
     *
     * @returns - The found resources list or **undefined** otherwise.
     */
    public getPath(path: string): ResourcesList | undefined {
        if (path == "") {
            return this._resourcesList || undefined;
        }

        return this.contains(path) ? resourcesListFindPath(this._resourcesList!, path) : undefined;
    }

    /**
     * Removes a path from the resources list.
     *
     * @param path - The path to remove.
     *
     * @returns - Whether the path was removed.
     */
    public removePath(path: string): boolean {
        if (!this._resourcesList) {
            return false;
        }

        if (path != this._root) {
            return resourcesListRemovePath(this._resourcesList, path);
        } else {
            this.clear();
            return true;
        }
    }

    /**
     * Checks whether a given path is contained in the cache.
     *
     * @param path - The path to check.
     */
    public contains(path: string): boolean {
        return !!this._resourcesList ? this._knownPaths.includes(path) : false;
    }

    /**
     * Whether the cache is empty.
     */
    public isEmpty(): boolean {
        return this._resourcesList == null;
    }

    /**
     * Clear the entire cache.
     */
    public clear(): void {
        this._resourcesList = null;
        this._knownPaths = [];
    }

    /**
     * The cached resources list.
     */
    public get resources(): ResourcesList | null {
        return this._resourcesList;
    }

    private isRoot(res: Resource): boolean {
        return res.type == ResourceType.Folder && res.filename == this._root;
    }

    private insertIntoParent(resources: ResourcesList, child: ResourcesList): boolean {
        // See if the current resources list contains the child
        for (let i = 0; i < resources.folders.length; ++i) {
            const folder = resources.folders[i]!;
            if (folder.resource.filename == child.resource.filename) {
                resources.folders[i] = child;
                return true;
            }

            // Only recurse deeper into the current sub-folder if the child's path starts with the folder's path
            if (child.resource.filename.startsWith(folder.resource.filename)) {
                return this.insertIntoParent(folder, child);
            }
        }

        return false;
    }

    private updateResourceSizes(): void {
        const _update = (resources: ResourcesList): void => {
            for (const folder of resources.folders) {
                _update(folder);
            }

            if (resources.resource.type == ResourceType.Folder) {
                if (this.contains(resources.resource.filename)) {
                    resources.resource.size = 0;

                    for (const folder of resources.folders) {
                        resources.resource.size += Math.max(0, folder.resource.size);
                    }
                    for (const file of resources.files) {
                        resources.resource.size += file.size;
                    }
                } else {
                    resources.resource.size = -1;
                }
            }
        };

        if (!!this._resourcesList) {
            _update(this._resourcesList);
        }
    }
}

/**
 * Cache to store resources lists based on their root path.
 *
 * This is used to store resources lists incrementally, i.d., the existing lists can be extended on demand.
 */
export class ResourcesListCache {
    private _cacheEntries: Record<string, ResourcesListCacheEntry> = {};

    /**
     * Retrieves the cache for a specific root, creating one if necessary.
     *
     * @param root - The root path.
     */
    public root(root: string): ResourcesListCacheEntry {
        if (!(root in this._cacheEntries)) {
            this._cacheEntries[root] = new ResourcesListCacheEntry(root);
        }
        return this._cacheEntries[root]!;
    }

    /**
     * Removes all cached lists.
     */
    public clear(): void {
        this._cacheEntries = {};
    }
}
