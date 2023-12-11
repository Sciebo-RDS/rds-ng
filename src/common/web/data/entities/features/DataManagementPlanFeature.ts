import { type ProjectFeatureID } from "../EntityTypes";
import { ProjectFeature } from "./ProjectFeature";

/**
 * Data class for the data management plan project feature.
 */
export class DataManagementPlanFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "dmp";
}
