import "../../assets/styles/tailwind-init.css";

import { type App, type Component as VueComponent, createApp } from "vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import { v4 as uuidv4 } from "uuid";

import { ComponentData } from "./ComponentData";
import { MetaInformation } from "./MetaInformation";
import logging from "../core/logging/Logging"
import { getDefaultSettings } from "../settings/DefaultSettings";
import { Configuration, type SettingsContainer } from "../utils/config/Configuration";
import { UnitID } from "../utils/UnitID";

/**
 * Base class for all web components.
 *
 * Web applications are always based on this class. It mainly maintains an instance of the ``Core``, but also stores general information
 * about the application itself and the entire project.
 *
 * Instances of this class are never created directly. Instead, always use the ``create`` method which performs all necessary initialization
 * tasks.
 */
export class Component {
    private static _instance: Component | null = null;

    private readonly _data: ComponentData;

    private readonly _vueApp: App;

    private constructor(env: SettingsContainer, compID: UnitID, appRoot: VueComponent, appElement: string) {
        Component._instance = this;

        compID = this.sanitizeComponentID(compID);

        let metaInfo = new MetaInformation();
        let compInfo = metaInfo.getComponent(compID.unit);

        this._data = new ComponentData(
            compID,
            this.createConfig(env),
            metaInfo.title,
            compInfo.name,
            metaInfo.version
        );

        logging.info(this.toString());
        logging.info("-- Starting component...");

        this._vueApp = this.createVueApp(appRoot, appElement);
    }

    private createConfig(env: SettingsContainer): Configuration {
        let config = new Configuration(env);
        config.addDefaults(getDefaultSettings());

        try {
            config.load();
        } catch (exc) {
            logging.warning("Component configuration could not be loaded", "core", { error: exc });
        }

        return config;
    }

    private createVueApp(appRoot: VueComponent, appElement: string): App {
        let app = createApp(appRoot);

        app.use(createPinia());
        app.use(PrimeVue);

        app.mount(appElement);

        return app;
    }

    /**
     * A data helper object that stores useful component data and information.
     */
    public get data(): ComponentData {
        return this._data;
    }

    /**
     * The global Vue application instance.
     */
    public get vue(): App {
        return this._vueApp;
    }

    /**
     * Creates a new web component.
     *
     * If an instance already exists, an error is thrown.
     *
     * @param env - The global environment variables.
     * @param compID - The identifier of this component.
     * @param appRoot - The Vue root component.
     * @param appElement - The HTML element ID used for mounting the root component.
     *
     * @throws Error - If an application instance has already been created.
     */
    public static create(env: SettingsContainer, compID: UnitID, appRoot: VueComponent, appElement: string = "#app"): Component {
        if (Component._instance !== null) {
            throw new Error("An application instance has already been created");
        }

        return new Component(env, compID, appRoot, appElement);
    }

    /**
     * The global ``Component`` instance.
     *
     * @throws Error - If no application instance has been created yet.
     */
    public static get instance(): Component {
        if (Component._instance === null) {
            throw new Error("No application instance has been created yet");
        }

        return Component._instance;
    }

    private sanitizeComponentID(compID: UnitID): UnitID {
        let instance: string = compID.instance !== undefined ? compID.instance : "default";
        let uniqueID = uuidv4();

        return new UnitID(compID.type, compID.unit, `${instance}::${uniqueID}`);
    }

    /**
     * @returns - The string representation of this component.
     */
    public toString(): string {
        return `${this._data.title} v${this._data.version}: ${this._data.name} (${this._data.compID})`;
    }
}
