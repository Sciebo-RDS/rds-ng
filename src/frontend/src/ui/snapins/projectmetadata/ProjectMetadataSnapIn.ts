import { SnapIn, type SnapInID } from "../SnapIn";

export class ProjectMetadataSnapIn extends SnapIn {
    public static readonly SnapInID: SnapInID = "metadata";

    public constructor() {
        super(ProjectMetadataSnapIn.SnapInID, {
            name: "Metadata",
            tabPanel: {
                label: "Metadata",
                loader: () => import("./ProjectMetadataPanel.vue"),
                description:
                    "This feature allows you to add metadata to your research data. It will be automatically added to your following research and publication process."
            }
        });
    }
}
