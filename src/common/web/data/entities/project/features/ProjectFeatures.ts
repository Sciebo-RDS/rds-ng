import { Type } from "class-transformer";

import { DataManagementPlanFeature } from "./DataManagementPlanFeature";
import { ProjectMetadataFeature } from "./ProjectMetadataFeature";
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
    @Type(() => ProjectMetadataFeature)
    public readonly project_metadata: ProjectMetadataFeature;
    // @ts-ignore
    @Type(() => ResourcesMetadataFeature)
    public readonly resources_metadata: ResourcesMetadataFeature;
    // @ts-ignore
    @Type(() => DataManagementPlanFeature)
    public readonly dmp: DataManagementPlanFeature;

    public constructor(projectMetadata?: ProjectMetadataFeature, resourceMetadata?: ResourcesMetadataFeature, dmp?: DataManagementPlanFeature) {
        this.project_metadata = projectMetadata || new ProjectMetadataFeature();
        this.resources_metadata = resourceMetadata || new ResourcesMetadataFeature();
        this.dmp = dmp || new DataManagementPlanFeature();
    }
}
