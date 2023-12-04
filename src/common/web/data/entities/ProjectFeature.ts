/**
 * The project  featureID type.
 */
export type FeatureID = string;

/**
 * Base data for a **Project** feature; specific features are derived from this class.
 *
 * A Project feature realizes the various aspects of a single project. Usually, a feature instance exists for each available feature to keep its data
 * even if the feature itself is disabled for the project. If a feature is missing (e.g., it was added at a later time), the feature is considered disabled
 * by default.
 *
 * @param feature_id - The feature identifier.
 * @param enabled - Whether the feature is enabled (activated) for the project.
 */
export abstract class ProjectFeature {
    public readonly feature_id: FeatureID;

    public readonly enabled: boolean;

    protected constructor(featureID: FeatureID, enabled: boolean = true) {
        this.feature_id = featureID;

        this.enabled = enabled;
    }
}
