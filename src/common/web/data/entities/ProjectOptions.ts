import { Type } from "class-transformer";

import { type ProjectFeatureID } from "./EntityTypes";

/**
 * Arbitrary UI options.
 */
export type UIOptions = Record<string, any>;

/**
 * Class holding all options of a **Project**.
 *
 * @param optional_features - A list of all user-enabled optional features.
 * @param ui - Arbitrary UI options.
 */
export class ProjectOptions {
    // @ts-ignore
    @Type(() => String)
    public readonly optional_features: ProjectFeatureID[];

    public readonly ui: UIOptions;

    public constructor(optionalFeatures: ProjectFeatureID[] = [], uiOptions: UIOptions = {}) {
        this.optional_features = optionalFeatures;

        this.ui = uiOptions;
    }
}
