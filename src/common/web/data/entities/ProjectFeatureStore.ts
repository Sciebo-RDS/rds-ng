/**
 * Base data class for a **Project** feature; specific features are derived from this class.
 *
 * A Project feature realizes the various aspects of a single project. Usually, a feature instance exists for each available feature to keep its data
 * even if the feature itself is disabled for the project. If a feature is missing (e.g., it was added at a later time), the feature is considered disabled
 * by default.
 */
export abstract class ProjectFeatureStore {
}
