import { LayoutPropertyObject } from "@common/ui/components/propertyeditor/PropertyObjectStore";
import { Type } from "class-transformer";
import { ProjectFeature, type ProjectFeatureID } from "./ProjectFeature";

/**
 * The DMP metadata type.
 *
 *
 */
export type DataManagementPlan = LayoutPropertyObject[];

/**
 * Data class for the data management plan project feature.
 */
export class DataManagementPlanFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "dmp";

    // @ts-ignore
    @Type(() => LayoutPropertyObject)
    public readonly plan: DataManagementPlan;

    public constructor(plan: DataManagementPlan = []) {
        super();

        this.plan = plan;
    }

    public get featureID(): ProjectFeatureID {
        return DataManagementPlanFeature.FeatureID;
    }
}
