import { SnapIn, type SnapInID } from "../SnapIn";

export class SummarySnapIn extends SnapIn {
    public static readonly SnapInID: SnapInID = "summary";

    public constructor() {
        super(SummarySnapIn.SnapInID, {
            name: "Summary",
            tabPanel: {
                label: "Summary",
                loader: () => import("./SummaryPanel.vue")
            }
        });
    }
}
