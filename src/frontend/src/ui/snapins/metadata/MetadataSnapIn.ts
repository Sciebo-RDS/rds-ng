import { SnapIn, SnapInFlags, type SnapInID } from "../SnapIn";

export class MetadataSnapIn extends SnapIn {
    public static readonly SnapInID: SnapInID = "metadata";

    public constructor() {
        super(MetadataSnapIn.SnapInID, {
            flags: SnapInFlags.Optional,
            displayName: "Project Metadata",
            optionName: "Project Metadata",
            tabPanel: () => import("./MetadataPanel.vue")
        });
    }
}
