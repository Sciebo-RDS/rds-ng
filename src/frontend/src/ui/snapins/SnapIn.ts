import { type ProjectFeatureID } from "@common/data/entities/project/features/ProjectFeature";

/**
 * The snap-in identifier type.
 */
export type SnapInID = string;

/**
 * Dynamic panel Vue component loader.
 */
export type SnapInPanelLoader = () => any;

/**
 * Options to initialize a snap-in.
 */
export interface SnapInOptions {
    /** The general display name. */
    name: string;

    /** Options specific to optional snap-ins (and their associated feature, if any). */
    optional?: {
        /** The label name of the option (shown as a checkbox) for this snap-in. */
        label: string;

        /** The ID of a directly associated project feature. If set, the associated feature will be en-/disabled alongside the snap-in. */
        feature?: ProjectFeatureID;
    };

    /** Tab-panel options. */
    tabPanel?: {
        /** The tab panel label name (displayed as its header). */
        label: string;

        /** The panel loader. */
        loader: SnapInPanelLoader;
    };
}

/**
 * A snap-in represents a certain feature aspect of a project that integrates itself automatically into the UI.
 */
export abstract class SnapIn {
    private readonly _snapInID: SnapInID;
    private readonly _options: SnapInOptions;

    /**
     * @param snapInID - The ID of the snap-in.
     * @param options - The snap-in options.
     */
    protected constructor(snapInID: SnapInID, options: SnapInOptions) {
        this._snapInID = snapInID;
        this._options = options;
    }

    /**
     * The ID of the snap-in.
     */
    public get snapInID(): SnapInID {
        return this._snapInID;
    }

    /**
     * The snap-in options.
     */
    public get options(): SnapInOptions {
        return this._options;
    }

    /**
     * Whether this snap-in is optional.
     */
    public isOptional(): boolean {
        return !!this._options.optional;
    }

    /**
     * Whether this snap-in has a tab panel.
     */
    public hasTabPanel(): boolean {
        return !!this._options.tabPanel;
    }
}
