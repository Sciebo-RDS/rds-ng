import { ProjectFeatureID } from "../data/entities/EntityTypes";

/**
 * Possible flags for a project feature.
 */
export const enum ProjectFeatureFlags {
    None = 0,

    Optional = 1 << 0
}

/**
 * A project feature containing meta information describing a single project feature.
 */
export abstract class ProjectFeature {
    private readonly _featureID: ProjectFeatureID;

    private readonly _flags: ProjectFeatureFlags;

    private readonly _displayName: string;
    private readonly _optionName: string;

    /**
     * @param featureID - The project feature ID.
     * @param flags - Feature flags.
     * @param displayName - The general display name.
     * @param optionName - The toggle-option name (only effective for optional features).
     */
    protected constructor(featureID: ProjectFeatureID, flags: ProjectFeatureFlags, displayName: string, optionName: string = "") {
        this._featureID = featureID;

        this._flags = flags;

        this._displayName = displayName;
        this._optionName = optionName;
    }

    /**
     * The project feature ID.
     */
    public get featureID(): ProjectFeatureID {
        return this._featureID;
    }

    /**
     * Check if certain flags are set.
     */
    public hasFlags(flags: ProjectFeatureFlags): boolean {
        return (this._flags & flags) === flags;
    }

    /**
     * The general display name.
     */
    public get displayName(): string {
        return this._displayName;
    }

    /**
     * he toggle-option name.
     */
    public get optionName(): string {
        return this._optionName;
    }
}
