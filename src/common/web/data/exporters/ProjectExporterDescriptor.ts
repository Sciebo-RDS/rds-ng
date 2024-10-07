import { Type } from "class-transformer";

import { type ProjectFeatureID } from "../entities/project/features/ProjectFeature";

/**
 * The exporter ID type.
 */
export type ProjectExporterID = string;

/**
 * Describes a project exporter. This class is used to easily transfer information about an exporter.
 *
 * @param exporter_id - The global exporter ID.
 * @param name - The display name.
 * @param description - The exporter's description.
 * @param extension - The extension of exported files.
 * @param scope - The scope where the exporter applies; if empty, it applies to the overall project.
 */
export class ProjectExporterDescriptor {
    public readonly exporter_id: ProjectExporterID;

    public readonly name: string;
    public readonly description: string;
    public readonly extension: string;

    // @ts-ignore
    @Type(() => String)
    public readonly scope: ProjectFeatureID[];

    public constructor(exporterID: ProjectExporterID, name: string, description: string, scope: ProjectFeatureID[]) {
        this.exporter_id = exporterID;

        this.name = name;
        this.description = description;

        this.scope = scope;
    }
}
