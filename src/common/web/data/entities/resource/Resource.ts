/**
 * The resource type.
 */
export enum ResourceType {
    Folder = "folder",
    File = "file",
}

/**
 * A single file or folder resource.
 *
 * @param filename - The complete name (path) of the resource.
 * @param basename - The name (w/o path) of the resource.
 * @param type - The type of the resource (folder or file).
 * @param size - The size of the resource; for folders, this is the size of all its contents.
 * @param mime_type - The MIME type of the resource.
 */
export class Resource {
    public readonly filename: string;
    public readonly basename: string;
    public readonly type: ResourceType;

    public readonly size: number;
    public readonly mime_type: string;

    public constructor(filename: string, basename: string, type: ResourceType, size: number = 0, mimeType: string = "") {
        this.filename = filename;
        this.basename = basename;
        this.type = type;

        this.size = size;
        this.mime_type = mimeType;
    }
}
