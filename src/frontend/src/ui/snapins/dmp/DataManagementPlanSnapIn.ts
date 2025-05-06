import { DataManagementPlanFeature } from "@common/data/entities/project/features/DataManagementPlanFeature";

import { SnapIn, type SnapInID } from "../SnapIn";

export class DataManagementPlanSnapIn extends SnapIn {
    public static readonly SnapInID: SnapInID = "dmp";

    public constructor() {
        super(DataManagementPlanSnapIn.SnapInID, {
            name: "Data Management Plan",
            optional: {
                label: "Data Management Plan",
                feature: DataManagementPlanFeature.FeatureID,
                description: "Activate this feature to implement all the steps needed for your project or grant application process."
            },
            tabPanel: {
                label: "Data Management Plan",
                loader: () => import("./DataManagementPlanPanel.vue"),
                description: "This feature allows you to implement all the steps needed for your project or grant application process."
            }
        });
    }
}
