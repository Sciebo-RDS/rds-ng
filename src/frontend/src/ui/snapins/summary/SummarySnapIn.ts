import { type SnapInID } from "@common/data/entities/EntityTypes";

import { SnapIn } from "../SnapIn";

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
