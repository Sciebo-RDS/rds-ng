import { type SnapInID } from "@common/data/entities/EntityTypes";
import { DataManagementPlanFeature } from "@common/data/entities/features/DataManagementPlanFeature";

import { SnapIn, SnapInFlags } from "../SnapIn";

export class DataManagementPlanSnapIn extends SnapIn {
    public static readonly SnapInID: SnapInID = "dmp";

    public constructor() {
        super(DataManagementPlanSnapIn.SnapInID, {
            flags: SnapInFlags.Optional,
            displayName: "Data Management Plan",
            optionName: "Data Management Plan",
            associatedFeature: DataManagementPlanFeature.FeatureID,
            tabPanel: () => import("./DataManagementPlanPanel.vue")
        });
    }
}
