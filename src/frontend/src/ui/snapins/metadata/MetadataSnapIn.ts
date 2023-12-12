import { type SnapInID } from "@common/data/entities/EntityTypes";
import { MetadataFeature } from "@common/data/entities/features/MetadataFeature";

import { SnapIn, SnapInFlags } from "../SnapIn";

export class MetadataSnapIn extends SnapIn {
    public static readonly SnapInID: SnapInID = "metadata";

    public constructor() {
        super(MetadataSnapIn.SnapInID, {
            flags: SnapInFlags.Optional,
            displayName: "Project Metadata",
            optionName: "Project Metadata",
            associatedFeature: MetadataFeature.FeatureID,
            tabPanel: () => import("./MetadataPanel.vue")
        });
    }
}
