import { ResourcesMetadataFeature } from "@common/data/entities/project/features/ResourcesMetadataFeature";

import { SnapIn, type SnapInID } from "../SnapIn";

export class ResourcesMetadataSnapIn extends SnapIn {
    public static readonly SnapInID: SnapInID = "resources_metadata";

    public constructor() {
        super(ResourcesMetadataSnapIn.SnapInID, {
            name: "Objects",
            optional: {
                label: "Object Descriptions",
                feature: ResourcesMetadataFeature.FeatureID
            },
            tabPanel: {
                label: "Objects",
                loader: () => /*import("./ResourcesMetadataPanel.vue")*/ null
            }
        });
    }
}
