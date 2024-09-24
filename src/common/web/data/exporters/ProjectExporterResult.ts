/**
 * Encapsulates the result of a project export.
 */
export class ProjectExporterResult {
    public readonly mimetype: string;

    public readonly data: ArrayBuffer;

    public constructor(mimetype: string, data: ArrayBuffer) {
        this.mimetype = mimetype;

        this.data = data;
    }
}
