import { SnapIn, SnapInFlags, type SnapInID } from "../SnapIn";

export class SummarySnapIn extends SnapIn {
    public static readonly SnapInID: SnapInID = "summary";

    public constructor() {
        super(SummarySnapIn.SnapInID, {
            flags: SnapInFlags.None,
            displayName: "Summary",
            optionName: "Summary",
            tabPanel: () => import("./SummaryPanel.vue")
        });
    }
}
