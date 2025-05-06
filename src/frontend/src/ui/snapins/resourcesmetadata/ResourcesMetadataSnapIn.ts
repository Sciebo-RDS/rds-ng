import { ResourcesMetadataFeature } from "@common/data/entities/project/features/ResourcesMetadataFeature";

import { SnapIn, type SnapInID } from "../SnapIn";

export class ResourcesMetadataSnapIn extends SnapIn {
    public static readonly SnapInID: SnapInID = "resources_metadata";

    public constructor() {
        super(ResourcesMetadataSnapIn.SnapInID, {
            name: "Data annotation",
            optional: {
                label: "Data annotation",
                feature: ResourcesMetadataFeature.FeatureID,
                description: "Activate this feature to set up an annotation infrastructure for your research data."
            },
            tabPanel: {
                label: "Data annotation",
                loader: () => import("./ResourcesMetadataPanel.vue"),
                description: "This feature allows you to set up an annotation infrastructure for your research data."
            }
        });
    }
}
