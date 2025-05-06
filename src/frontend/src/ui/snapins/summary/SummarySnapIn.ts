import { SnapIn, type SnapInID } from "../SnapIn";

export class SummarySnapIn extends SnapIn {
    public static readonly SnapInID: SnapInID = "summary";

    public constructor() {
        super(SummarySnapIn.SnapInID, {
            name: "Overview",
            tabPanel: {
                label: "Overview",
                loader: () => import("./SummaryPanel.vue"),
                description: "An overview and general statistics about your project."
            }
        });
    }
}
