import { Type } from "class-transformer";

import { type ProjectFeatureID, type SnapInID } from "./EntityTypes";

/**
 * Class holding all options of a **Project**.
 *
 * @param optional_features - A list of all user-enabled optional features.
 * @param optional_snapins - A list of all user-enabled optional UI snap-ins.
 */
export class ProjectOptions {
    // @ts-ignore
    @Type(() => String)
    public readonly optional_features: ProjectFeatureID[];

    // @ts-ignore
    @Type(() => String)
    public readonly optional_snapins: SnapInID[];

    public constructor(optionalFeatures: ProjectFeatureID[] = [], optionalSnapIns: SnapInID[] = []) {
        this.optional_features = optionalFeatures;
        this.optional_snapins = optionalSnapIns;
    }
}
