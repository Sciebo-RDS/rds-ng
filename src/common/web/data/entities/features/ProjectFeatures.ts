import { Type } from "class-transformer";

import { type ProjectFeatureID } from "../EntityTypes";
import { DataManagementPlanFeature } from "./DataManagementPlanFeature";
import { MetadataFeature } from "./MetadataFeature";

/**
 * Superordinate data for all **Project** features.
 *
 * @param metadata - The metadata project feature.
 * @param dmp - The data management plan feature.
 * @param optional_features - A list of all user-enabled optional features (this might include features that are only present in the UI bot not the backend).
 */
export class ProjectFeatures {
    // @ts-ignore
    @Type(() => MetadataFeature)
    public readonly metadata: MetadataFeature;
    // @ts-ignore
    @Type(() => DataManagementPlanFeature)
    public readonly dmp: DataManagementPlanFeature;

    // @ts-ignore
    @Type(() => String)
    public readonly optional_features: ProjectFeatureID[];

    public constructor(metadata: MetadataFeature = new MetadataFeature(), dmp: DataManagementPlanFeature = new DataManagementPlanFeature(), optionalFeatures: ProjectFeatureID[] = []) {
        this.metadata = metadata;
        this.dmp = dmp;

        this.optional_features = optionalFeatures;
    }
}
