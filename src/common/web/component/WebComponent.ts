import "../../assets/styles/tailwind-init.css";

import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
// @ts-ignore
import { v4 as uuidv4 } from "uuid";
import { type App, type Component as VueComponent, createApp, inject } from "vue";

import { Core } from "../core/Core";
import logging from "../core/logging/Logging"
import { Service } from "../services/Service";
import { ServiceContext } from "../services/ServiceContext";
import { getDefaultSettings } from "../settings/DefaultSettings";
import { Configuration, type SettingsContainer } from "../utils/config/Configuration";
import { type Constructable } from "../utils/Types";
import { UnitID } from "../utils/UnitID";
import { MetaInformation } from "./MetaInformation";
import { WebComponentData } from "./WebComponentData";

import createComponentService from "../services/ComponentService";
import createNetworkService from "../services/NetworkService";

// Necessary to make the entire API known
import "../api/API";

/**
 * Base class for all web components.
 *
 * Web applications are always based on this class. It mainly maintains an instance of the ``Core``, but also stores general information
 * about the application itself and the entire project.
 *
 * Instances of this class are never created directly. Instead, always use the ``create`` method which performs all necessary initialization
 * tasks.
 */
export class WebComponent {
    private static _instance: WebComponent | null = null;
    private static readonly _injectionKey = Symbol();

    private readonly _data: WebComponentData;

    private readonly _core: Core;
    private readonly _vueApp: App;

    private constructor(env: SettingsContainer, compID: UnitID, appRoot: VueComponent, appElement: string) {
        if (WebComponent._instance) {
            throw new Error("A component instance has already been created")
        }
        WebComponent._instance = this;

        compID = this.sanitizeComponentID(compID);

        let metaInfo = new MetaInformation();
        let compInfo = metaInfo.getComponent(compID.unit);

        this._data = new WebComponentData(
            compID,
            this.createConfig(env),
            metaInfo.title,
            compInfo.name,
            metaInfo.version
        );

        logging.info(this.toString());
        logging.info("-- Starting component...");

        this._core = new Core(this._data);
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
        logging.info("-- Creating Vue application...");

        let app = createApp(appRoot);

        app.use(createPinia());
        app.use(PrimeVue);

        app.provide(WebComponent._injectionKey, this);

        app.mount(appElement);

        return app;
    }

    /**
     * Starts the component's execution cycles.
     *
     * Notes:
     *     It is mandatory to call this method after creating and setting up a component.
     */
    public run(): void {
        logging.info("Running component...");

        // Create all basic services
        createComponentService(this);
        createNetworkService(this);

        this._core.run();
    }

    /**
     * Creates and registers a new service.
     *
     * @param name - The name of the service.
     * @param initializer - A function called to registered message handlers etc. after the service has been created.
     * @param contextType - Can be used to override the default ``ServiceContext`` type. All message handlers
     *      associated with the new service will then receive instances of this type for their service context.
     */
    public createService<CtxType extends ServiceContext>(name: string,
                                                         initializer: ((svc: Service) => void) | null = null,
                                                         contextType: Constructable<CtxType> = ServiceContext as Constructable<CtxType>): Service {
        let svc = new Service<CtxType>(this._data.compID, name, this._core.messageBus, contextType);
        this._core.registerService(svc);
        if (initializer) {
            initializer(svc);
        }
        return svc;
    }

    /**
     * A data helper object that stores useful component data and information.
     */
    public get data(): WebComponentData {
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
     * @returns - The newly created component.
     */
    public static create(env: SettingsContainer, compID: UnitID, appRoot: VueComponent, appElement: string = "#app"): WebComponent {
        return new WebComponent(env, compID, appRoot, appElement);
    }

    /**
     * The global ``WebComponent`` instance via Vue's injection mechanism.
     *
     * @throws Error - If no instance has been created.
     */
    public static inject(): WebComponent {
        let inst = inject<WebComponent>(WebComponent._injectionKey);
        if (!inst) {
            throw new Error("No component instance has been created");
        }
        return inst;
    }

    /**
     * The global ``WebComponent`` instance.
     *
     * @throws Error - If no instance has been created.
     */
    public static get instance(): WebComponent {
        if (!WebComponent._instance) {
            throw new Error("No component instance has been created");
        }
        return WebComponent._instance;
    }

    private sanitizeComponentID(compID: UnitID): UnitID {
        let instance: string = compID.instance ? compID.instance : "default";
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
