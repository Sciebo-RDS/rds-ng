import { Type } from "class-transformer";

import { SharedPropertyObject } from "../../../../ui/components/propertyeditor/PropertyObjectStore";
import { type MetadataObjects } from "../../metadata/Types";
import { DataManagementPlanFeature } from "./DataManagementPlanFeature";
import { ProjectMetadataFeature } from "./ProjectMetadataFeature";
import { ResourcesMetadataFeature } from "./ResourcesMetadataFeature";

/**
 * Superordinate data for all **Project** features.
 *
 * @param metadata - The metadata project feature.
 * @param resources_metadata - The resources metadata project feature.
 * @param dmp - The data management plan feature.
 * @param shared_objects - Project-wide shared metadata objects.
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

    // @ts-ignore
    @Type(() => SharedPropertyObject)
    public readonly shared_objects: MetadataObjects;

    public constructor(
        projectMetadata?: ProjectMetadataFeature,
        resourceMetadata?: ResourcesMetadataFeature,
        dmp?: DataManagementPlanFeature,
        sharedPropertyObjects?: MetadataObjects
    ) {
        this.project_metadata = projectMetadata || new ProjectMetadataFeature();
        this.resources_metadata = resourceMetadata || new ResourcesMetadataFeature();
        this.dmp = dmp || new DataManagementPlanFeature();

        this.shared_objects = sharedPropertyObjects || [];
    }
}
