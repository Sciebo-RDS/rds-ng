import { MetadataFeature } from "@common/data/entities/features/MetadataFeature";

import { SnapIn, type SnapInID } from "../SnapIn";

export class MetadataSnapIn extends SnapIn {
    public static readonly SnapInID: SnapInID = "metadata";

    public constructor() {
        super(MetadataSnapIn.SnapInID, {
            name: "Project Metadata",
            optional: {
                label: "Project Metadata",
                feature: MetadataFeature.FeatureID
            },
            tabPanel: {
                label: "Project Metadata",
                loader: () => import("./MetadataPanel.vue")
            }
        });
    }
}
