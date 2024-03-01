import { PropertyController } from "../PropertyController";
import { PropertySet } from "../PropertySet";

/**
 * The exporter identifier type.
 */
export type ExporterID = string;

/**
 * Dynamic MenuItem Vue component loader.
 */
export type ExporterDownloader = (controller: PropertyController<PropertySet | PropertySet[]>, title: string) => any;

/**
 * Options to initialize a exporter.
 */
export interface ExporterOptions {
    /** The general display name. */
    name: string;

    /** Whether this Export is used for DMPs */
    Dmp: boolean;

    menuItem: {
        /** The menu item label name. */
        label: string;
        /** The menu item icon. */
        icon: string;

        /** The Export Download function */
        command: ExporterDownloader;
    };
}

/**
 * A exporter represents a certain feature aspect of a project that integrates itself automatically into the UI.
 */
export abstract class Exporter {
    private readonly _exporterID: ExporterID;
    private readonly _options: ExporterOptions;

    /**
     * @param exporterID - The ID of the exporter.
     * @param options - The exporter options.
     */
    protected constructor(exporterID: ExporterID, options: ExporterOptions) {
        this._exporterID = exporterID;
        this._options = options;
    }

    /**
     * The ID of the exporter.
     */
    public get exporterID(): ExporterID {
        return this._exporterID;
    }

    /**
     * The exporter options.
     */
    public get options(): ExporterOptions {
        return this._options;
    }
}
