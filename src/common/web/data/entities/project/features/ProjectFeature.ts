/**
 * The project feature identifier type.
 */
export type ProjectFeatureID = string;

/**
 * Base data class for a project feature.
 */
export abstract class ProjectFeature {
    /**
     * The ID of this feature.
     */
    public abstract get featureID(): ProjectFeatureID;
}
