import { FilesFeature } from "@common/data/entities/project/features/FilesFeature";

import { SnapIn, type SnapInID } from "../SnapIn";

export class FilesSnapIn extends SnapIn {
    public static readonly SnapInID: SnapInID = "files";

    public constructor() {
        super(FilesSnapIn.SnapInID, {
            name: "Objects",
            optional: {
                label: "Object Descriptions",
                feature: FilesFeature.FeatureID
            },
            tabPanel: {
                label: "Objects",
                loader: () => import("./FilesPanel.vue")
            }
        });
    }
}
