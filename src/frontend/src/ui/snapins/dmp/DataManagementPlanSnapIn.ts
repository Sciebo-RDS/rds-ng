import { type SnapInID } from "@common/data/entities/EntityTypes";
import { DataManagementPlanFeature } from "@common/data/entities/features/DataManagementPlanFeature";

import { SnapIn } from "../SnapIn";

export class DataManagementPlanSnapIn extends SnapIn {
    public static readonly SnapInID: SnapInID = "dmp";

    public constructor() {
        super(DataManagementPlanSnapIn.SnapInID, {
            name: "Data Management Plan",
            optional: {
                label: "Data Management Plan",
                feature: DataManagementPlanFeature.FeatureID
            },
            tabPanel: {
                label: "Data Management Plan",
                loader: () => import("./DataManagementPlanPanel.vue")
            }
        });
    }
}
