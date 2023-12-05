import { type Component as VueComponent, defineAsyncComponent } from "vue";

import { type ProjectFeatureID } from "../data/entities/EntityTypes";

/**
 * Possible flags for a project feature.
 */
export const enum ProjectFeatureFlags {
    None = 0,

    // Optional features can be turned on or off for a project
    Optional = 1 << 0,

    // Whether the feature has a display panel (shown as a tab)
    HasPanel = 1 << 1
}

/**
 * Options to initialize a project feature.
 */
export interface ProjectFeatureOptions {
    /** Feature flags. */
    flags: ProjectFeatureFlags;

    /** The general display name. */
    displayName: string;
    /** The toggle-option name (only effective for optional features). */
    optionName?: string;

    /** If a Vue component loader is specified, it will be used to load the feature's panel dynamically. */
    panel?: () => any;
}

/**
 * A project feature containing meta information describing a single project feature.
 */
export abstract class ProjectFeature {
    private readonly _featureID: ProjectFeatureID;

    private readonly _flags: ProjectFeatureFlags;

    private readonly _displayName: string;
    private readonly _optionName: string;

    private readonly _panel: VueComponent | undefined = undefined;

    /**
     * @param featureID - The project feature ID.
     * @param options - The feature options.
     */
    protected constructor(featureID: ProjectFeatureID, options: ProjectFeatureOptions) {
        this._featureID = featureID;

        this._flags = options.flags;

        this._displayName = options.displayName;
        this._optionName = options.optionName || "";

        if (options.panel) {
            this._panel = defineAsyncComponent(options.panel);
        }
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
     * The toggle-option name.
     */
    public get optionName(): string {
        return this._optionName;
    }

    /**
     * The feature's panel.
     */
    public get panel(): VueComponent | undefined {
        return this._panel;
    }
}
