import { Type } from "class-transformer";

import { DataManagementPlanFeature } from "./DataManagementPlanFeature";
import { FilesFeature } from "./FilesFeature";
import { MetadataFeature } from "./MetadataFeature";

/**
 * Superordinate data for all **Project** features.
 *
 * @param metadata - The metadata project feature.
 * @param dmp - The data management plan feature.
 */
export class ProjectFeatures {
    // @ts-ignore
    @Type(() => MetadataFeature)
    public readonly metadata: MetadataFeature;
    // @ts-ignore
    @Type(() => FilesFeature)
    public readonly files: FilesFeature;
    // @ts-ignore
    @Type(() => DataManagementPlanFeature)
    public readonly dmp: DataManagementPlanFeature;

    public constructor(
        metadata: MetadataFeature = new MetadataFeature(),
        files: FilesFeature = new FilesFeature(),
        dmp: DataManagementPlanFeature = new DataManagementPlanFeature()
    ) {
        this.metadata = metadata;
        this.files = files;
        this.dmp = dmp;
    }
}
