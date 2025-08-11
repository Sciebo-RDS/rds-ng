import { Type } from "class-transformer";

import { LayoutPropertyObject } from "../../../../ui/components/propertyeditor/PropertyObjectStore";
import { type ProfileID } from "../../../../ui/components/propertyeditor/PropertyProfile";
import { ProjectFeature, type ProjectFeatureID } from "./ProjectFeature";

/**
 * The project metadata type.
 *
 *
 */
export type ProjectMetadata = LayoutPropertyObject[];

/**
 * Data class for the metadata project feature.
 */
export class ProjectMetadataFeature extends ProjectFeature {
    public static readonly FeatureID: ProjectFeatureID = "project_metadata";

    // @ts-ignore
    @Type(() => LayoutPropertyObject)
    public readonly metadata: ProjectMetadata;

    public constructor(metadata: ProjectMetadata = [], enabledProfiles: ProfileID[] = []) {
        super(enabledProfiles);

        this.metadata = metadata;
    }

    public get featureID(): ProjectFeatureID {
        return ProjectMetadataFeature.FeatureID;
    }
}
