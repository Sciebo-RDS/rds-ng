import { Type } from "class-transformer";

import { Resource } from "./Resource";

/**
 * A list of resource folders.
 */
export type ResourceFolders = ResourcesList[];

/**
 * A list of resource files.
 */
export type ResourceFiles = Resource[];

/**
 * A recursive list of resources.
 *
 * Resources are always given in absolute form.
 *
 * @param resource - The current resource path.
 * @param folders - A list of all folders.
 * @param files - A list of all files.
 */
export class ResourcesList {
    public readonly resource: Resource;

    // @ts-ignore
    @Type(() => ResourcesList)
    public readonly folders: ResourceFolders;
    // @ts-ignore
    @Type(() => Resource)
    public readonly files: ResourceFiles;

    public constructor(resource: Resource, folders: ResourceFolders = [], files: ResourceFiles = []) {
        this.resource = resource;

        this.folders = folders;
        this.files = files;
    }
}
