import { Type } from "class-transformer";

import { type ProjectFeatureID } from "../entities/project/features/ProjectFeature";

/**
 * The exporter ID type.
 */
export type ProjectExporterID = string;

/**
 * Flags specifying extended capabilities of the exporter.
 */
export const enum ProjectExporterCapabilities {
    None = 0,
    AutoExport = 0x0001
}

/**
 * Describes a project exporter. This class is used to easily transfer information about an exporter.
 *
 * @param exporter_id - The global exporter ID.
 * @param name - The display name.
 * @param description - The exporter's description.
 * @param extension - The extension of exported files.
 * @param scope - The scope where the exporter applies; if empty, it applies to the overall project.
 * @param defaultScope - A default scope when exporting if none is given.
 * @param defaultFilename - A default filename used when none is given.
 */
export class ProjectExporterDescriptor {
    public readonly exporter_id: ProjectExporterID;

    public readonly name: string;
    public readonly description: string;
    public readonly extension: string;

    // @ts-ignore
    @Type(() => String)
    public readonly scope: ProjectFeatureID[];

    public readonly capabilities: ProjectExporterCapabilities;

    public readonly default_scope: ProjectFeatureID | undefined;
    public readonly default_filename: string;

    public constructor(
        exporterID: ProjectExporterID,
        name: string,
        description: string,
        extension: string,
        scope: ProjectFeatureID[],
        capabilities: ProjectExporterCapabilities = ProjectExporterCapabilities.None,
        defaultScope: ProjectFeatureID | undefined = undefined,
        defaultFilename: string = ""
    ) {
        this.exporter_id = exporterID;

        this.name = name;
        this.description = description;
        this.extension = extension;

        this.scope = scope;

        this.capabilities = capabilities;

        this.default_scope = defaultScope;
        this.default_filename = defaultFilename;
    }
}
