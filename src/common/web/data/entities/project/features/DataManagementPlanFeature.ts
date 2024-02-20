import { ProjectFeature, type ProjectFeatureID } from "./ProjectFeature";

/**
 * The DMP metadata type.
 *
 * TODO: Use proper type
 */
export type DataManagementPlan = Record<string, any>;

/**
 * Data class for the data management plan project feature.
 */
export class DataManagementPlanFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "dmp";

    public readonly dmp: DataManagementPlan = {};

    public constructor(dmp: DataManagementPlan = {}) {
        super();

        this.dmp = dmp;
    }
}
