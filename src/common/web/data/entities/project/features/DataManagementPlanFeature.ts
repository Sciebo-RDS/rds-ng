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

    public readonly plan: DataManagementPlan;

    public constructor(plan: DataManagementPlan = {}) {
        super();

        this.plan = plan;
    }

    public get featureID(): ProjectFeatureID {
        return DataManagementPlanFeature.FeatureID;
    }
}
