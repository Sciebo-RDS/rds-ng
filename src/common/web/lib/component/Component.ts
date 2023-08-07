import "../../assets/styles/tailwind-init.css";

import { App, createApp } from "vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import { ComponentData } from "./ComponentData";
import { MetaInformation } from "./MetaInformation";
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

    private readonly _data: ComponentData | null = null;

    private readonly _vueApp: App<HostElement> | null = null;

    private constructor(compID: UnitID, appRoot: Component, appElement: string) {
        Component._instance = this;

        compID = this.sanitizeComponentID(compID);

        let metaInfo = new MetaInformation();
        let compInfo = metaInfo.getComponent(compID.unit);

        this._data = new ComponentData(
            compID,
            metaInfo.title,
            compInfo["name"],
            metaInfo.version
        );
        console.log(this.toString());

        this._vueApp = this.createVueApp(appRoot, appElement);
    }

    private createVueApp(appRoot: Component, appElement: string) {
        let app = createApp(appRoot);

        app.use(createPinia());
        app.use(PrimeVue);

        app.mount(appElement);

        return app;
    }

    /**
     * A data helper object that stores useful component data and information.
     */
    public get data() {
        return this._data;
    }

    /**
     * The global Vue application instance.
     */
    public get vue() {
        return this._vueApp;
    }

    /**
     * Creates a new web component.
     *
     * If an instance already exists, an error is thrown.
     *
     * @param compID - The identifier of this component.
     * @param appRoot - The Vue root component.
     * @param appElement - The HTML element ID used for mounting the root component.
     *
     * @throws Error - If an application instance has already been created.
     */
    public static create(compID: UnitID, appRoot: Component, appElement: string = "#app") {
        if (Component._instance !== null) {
            throw new Error("An application instance has already been created");
        }

        return new Component(compID, appRoot, appElement);
    }

    /**
     * The global ``Component`` instance.
     */
    public static get instance() {
        if (Component._instance === null) {
            throw new Error("No application instance has been created yet");
        }

        return Component._instance;
    }

    private sanitizeComponentID(compID: UnitID) {
        if (compID.instance === undefined) {
            // TODO: Get from config
            return new UnitID(compID.type, compID.unit, "default");
        }

        return compID;
    }

    /**
     * @returns - The string representation of this component.
     */
    public toString() {
        return `${this._data.title} v${this._data.version}: ${this._data.name} (${this._data.compID})`;
    }
}
