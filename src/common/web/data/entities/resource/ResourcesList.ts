import { Type, Transform, plainToInstance } from "class-transformer";

import { type Resource } from "./Resource";

/**
 * A map of resource folders.
 */
export type ResourceFolders = Record<Resource, ResourcesList | undefined>;

/**
 * A recursive list of resources.
 *
 * Resources are always given in absolute form.
 *
 * @param resource - The current resource path.
 * @param folders - A dictionary containing all folders and their respective sub-folder contents (can be **undefined**).
 * @param files - A list of all files.
 */
export class ResourcesList {
    public readonly resource: Resource;

    // @ts-ignore
    @Transform(({ value, key, obj, type }) => {
        for (const [k, v] of Object.entries(value)) {
            value[k] = plainToInstance(ResourcesList, v);
        }
        return value;
    })
    public readonly folders: ResourceFolders;
    // @ts-ignore
    @Type(() => String)
    public readonly files: ResourceFiles;

    public constructor(resource: Resource, folders: ResourceFolders = {}, files: ResourceFiles = []) {
        this.resource = resource;

        this.folders = folders;
        this.files = files;
    }
}
