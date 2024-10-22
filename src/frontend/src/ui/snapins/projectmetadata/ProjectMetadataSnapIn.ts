import { ProjectMetadataFeature } from "@common/data/entities/project/features/ProjectMetadataFeature";

import { SnapIn, type SnapInID } from "../SnapIn";

export class ProjectMetadataSnapIn extends SnapIn {
    public static readonly SnapInID: SnapInID = "metadata";

    public constructor() {
        super(ProjectMetadataSnapIn.SnapInID, {
            name: "Project Metadata",
            optional: {
                label: "Project Metadata",
                feature: ProjectMetadataFeature.FeatureID
            },
            tabPanel: {
                label: "Project Metadata",
                loader: () => import("./ProjectMetadataPanel.vue")
            }
        });
    }
}
