import { SnapIn, SnapInFlags, type SnapInID } from "../SnapIn";

export class DataManagementPlanSnapIn extends SnapIn {
    public static readonly SnapInID: SnapInID = "dmp";

    public constructor() {
        super(DataManagementPlanSnapIn.SnapInID, {
            flags: SnapInFlags.Optional,
            displayName: "Data Management Plan",
            optionName: "Data Management Plan",
            tabPanel: () => import("./DataManagementPlanPanel.vue")
        });
    }
}
