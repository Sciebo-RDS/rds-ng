import { Resource } from "@common/data/entities/resource/Resource";

class ResourcesDataCacheEntry {
    private readonly _resource: Resource;
    private readonly _data: ArrayBuffer;

    constructor(resource: Resource, data: ArrayBuffer) {
        this._resource = resource;
        this._data = data;
    }

    public get resource(): Resource {
        return this._resource;
    }

    public get data(): ArrayBuffer {
        return this._data;
    }
}

/**
 * Cache to store the data of resources.
 *
 * The cache has space for a certain number of items, removing old elements when necessary.
 */
export class ResourcesDataCache {
    private readonly _cache: ResourcesDataCacheEntry[] = [];
    private readonly _capacity: number;

    public constructor(capacity: number = 100) {
        this._capacity = Math.max(capacity, 10);
    }

    /**
     * Add a new element to the cache.
     *
     * If an entry for the resource already exists, it will simply be moved to the end of the cache. Otherwise,
     * a new element will be added, potentially removing old ones to stay within its capacity.
     *
     * @param resource - The resource to add.
     * @param data - The resource data.
     */
    public push(resource: Resource, data: ArrayBuffer): void {
        if (this.hasData(resource)) {
            this.bump(resource);
        } else {
            this._cache.push(new ResourcesDataCacheEntry(resource, data));
            this.reduce();
        }
    }

    /**
     * Checks if data is available for a given resource.
     *
     * @param resource - The resource.
     */
    public hasData(resource: Resource): boolean {
        return !!this.findEntry(resource);
    }

    /**
     * Gets the data stored for a given resource.
     *
     * @param resource - The resource.
     *
     * @returns - The resource data.
     * @throws Error - If no data exists for the resource.
     */
    public getData(resource: Resource): ArrayBuffer {
        const entry = this.findEntry(resource);
        if (entry) {
            return entry.data;
        }
        throw new Error("Tried to access unexisting resource data");
    }

    /**
     * Moves a resource to the end of the cache to mark it as "new."
     *
     * @param resource - The resource to bump.
     */
    public bump(resource: Resource): void {
        const entry = this.findEntry(resource);
        if (entry) {
            const index = this._cache.indexOf(entry);
            this._cache.splice(index, 1);
            this._cache.push(entry);
        }
    }

    private findEntry(resource: Resource): ResourcesDataCacheEntry | null {
        for (const entry of this._cache) {
            if (entry.resource.filename == resource.filename) {
                return entry;
            }
        }
        return null;
    }

    private reduce(): void {
        while (this._cache.length > this._capacity) {
            this._cache.shift();
        }
    }
}
