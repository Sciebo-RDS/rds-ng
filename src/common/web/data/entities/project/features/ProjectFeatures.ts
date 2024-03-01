import { Type } from "class-transformer";

import { DataManagementPlanFeature } from "./DataManagementPlanFeature";
import { MetadataFeature } from "./MetadataFeature";
import { ResourcesMetadataFeature } from "./ResourcesMetadataFeature";

/**
 * Superordinate data for all **Project** features.
 *
 * @param metadata - The metadata project feature.
 * @param resources_metadata - The resources metadata project feature.
 * @param dmp - The data management plan feature.
 */
export class ProjectFeatures {
    // @ts-ignore
    @Type(() => MetadataFeature)
    public readonly metadata: MetadataFeature;
    // @ts-ignore
    @Type(() => ResourcesMetadataFeature)
    public readonly resources_metadata: ResourcesMetadataFeature;
    // @ts-ignore
    @Type(() => DataManagementPlanFeature)
    public readonly dmp: DataManagementPlanFeature;

    public constructor(
        metadata?: MetadataFeature,
        resourceMetadata?: ResourcesMetadataFeature,
        dmp?: DataManagementPlanFeature
    ) {
        this.metadata = metadata || new MetadataFeature();
        this.resources_metadata = resourceMetadata || new ResourcesMetadataFeature();
        this.dmp = dmp || new DataManagementPlanFeature();
    }
}
