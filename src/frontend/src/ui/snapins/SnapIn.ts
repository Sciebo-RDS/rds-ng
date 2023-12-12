import { type ProjectFeatureID, type SnapInID } from "@common/data/entities/EntityTypes";

import { type Component as VueComponent, defineAsyncComponent } from "vue";

/**
 * Dynamic panel Vue component loader.
 */
export type SnapInPanelLoader = () => any;

/**
 * Possible flags for a snap-in.
 */
export const enum SnapInFlags {
    None = 0,

    // Optional snap-ins can be turned on or off for a project
    Optional = 1 << 0,

    // Whether a project feature is directly associated with this snap-in
    HasAssociatedFeature = 1 << 1,
    // Whether the snap-in has a tab panel
    HasTabPanel = 1 << 2
}

/**
 * Options to initialize a snap-in.
 */
export interface SnapInOptions {
    /** Snap-In flags. */
    flags: SnapInFlags;

    /** The general display name. */
    displayName: string;
    /** The toggle-option name (only effective for optional snap-ins). */
    optionName?: string;

    /** The ID of a directly associated project feature. */
    associatedFeature?: ProjectFeatureID;

    /** If a Vue component loader is specified, it will be used to load the snap-in's tab panel dynamically. */
    tabPanel?: SnapInPanelLoader;
}

/**
 * A snap-in represents a certain feature aspect of a project that integrates itself automatically into the UI.
 */
export abstract class SnapIn {
    private readonly _snapInID: SnapInID;

    private readonly _flags: SnapInFlags;

    private readonly _displayName: string;
    private readonly _optionName: string;

    private readonly _associatedFeature: ProjectFeatureID | undefined = undefined;

    private readonly _tabPanel: VueComponent | undefined = undefined;

    /**
     * @param snapInID - The ID of the snap-in.
     * @param options - The snap-in options.
     */
    protected constructor(snapInID: SnapInID, options: SnapInOptions) {
        this._snapInID = snapInID;

        this._flags = options.flags;

        this._displayName = options.displayName;
        this._optionName = options.optionName || "";

        this._associatedFeature = options.associatedFeature;

        if (options.tabPanel) {
            this._flags |= SnapInFlags.HasTabPanel;
            this._tabPanel = defineAsyncComponent(options.tabPanel);
        }
    }

    /**
     * The ID of the snap-in.
     */
    public get snapInID(): SnapInID {
        return this._snapInID;
    }

    /**
     * Check if certain flags are set.
     */
    public hasFlags(flags: SnapInFlags): boolean {
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
     * The ID of a directly associated project feature.
     */
    public get associatedFeature(): ProjectFeatureID | undefined {
        return this._associatedFeature;
    }

    /**
     * The snap-in's tab panel.
     */
    public get tabPanel(): VueComponent | undefined {
        return this._tabPanel;
    }
}
