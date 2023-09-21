import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
// @ts-ignore
import { v4 as uuidv4 } from "uuid";
import { type App, type Component as VueComponent, createApp, inject } from "vue";
import { createRouter, createWebHistory, type Router, type RouteRecordRaw } from "vue-router";

import { Core } from "../core/Core";
import logging from "../core/logging/Logging"

import { Service } from "../services/Service";
import { ServiceContext } from "../services/ServiceContext";
import { getDefaultSettings } from "../settings/DefaultSettings";
import { MainView } from "../ui/views/main/MainView";
import { Configuration, type SettingsContainer } from "../utils/config/Configuration";
import { type Constructable } from "../utils/Types";
import { UnitID } from "../utils/UnitID";
import { MetaInformation } from "./MetaInformation";
import { WebComponentData } from "./WebComponentData";

import createComponentService from "../services/ComponentService";
import createNetworkService from "../services/NetworkService";
import createWebService from "../services/WebService";

import MainContainer from "../ui/views/main/MainViewContainer.vue";

// Load various icons
import "material-icons/iconfont/outlined.css";
import "primeicons/primeicons.css";

// Necessary to make the entire API known
import "../api/API";

/**
 * Base class for all web components.
 *
 * Web applications are always based on this class. It mainly maintains an instance of the ``Core``, but also stores general information
 * about the application itself and the entire project.
 */
export class WebComponent {
    private static _instance: WebComponent | null = null;
    private static readonly _injectionKey = Symbol();

    protected readonly _data: WebComponentData;

    protected readonly _core: Core;
    protected readonly _router: Router;

    protected readonly _mainView: MainView;
    protected readonly _vueApp: App;

    /**
     * @param env - The global environment variables.
     * @param compID - The identifier of this component.
     * @param appRoot - The root (main) application component.
     */
    public constructor(env: SettingsContainer, compID: UnitID, appRoot: VueComponent) {
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
        this._router = this.createRouter();

        this._mainView = new MainView(this._router, appRoot);
        this._vueApp = this.createVueApp();
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

    private createRouter(): Router {
        return createRouter({
            history: createWebHistory(),
            routes: [...this.configureDefaultRoutes(), ...this.configureRoutes()],
        });
    }

    private createVueApp(): App {
        logging.info("-- Creating Vue application...");

        const app = createApp(MainContainer);

        app.use(createPinia());
        app.use(this._router);
        app.use(PrimeVue);

        app.provide(WebComponent._injectionKey, this);

        return app;
    }

    private configureDefaultRoutes(): RouteRecordRaw[] {
        return [];
    }

    /**
     * Sets up routes for the Vue router.
     *
     * @returns - The routes as an array; return `null` if the router shouldn't be used.
     */
    protected configureRoutes(): RouteRecordRaw[] {
        return [];
    }

    /**
     * Mounts the Vue application in the given element.
     *
     * Notes:
     *     This method must be called immediately after creating the main component instance.
     *
     * @param appElement - The HTML element ID used for mounting the root component.
     */
    public mount(appElement: string = "#app"): void {
        this._vueApp.mount(appElement);
    }

    /**
     * Starts the component's execution cycles.
     *
     * Notes:
     *     This method is automatically called by the framework.
     */
    public run(): void {
        logging.info("Running component...");

        // Create all basic services
        createComponentService(this);
        createNetworkService(this);
        createWebService(this);

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
     * The global router.
     */
    public get router(): Router {
        return this._router;
    }

    /**
     * The global main view.
     */
    public get mainView(): MainView {
        return this._mainView;
    }

    /**
     * The global Vue application instance.
     */
    public get vue(): App {
        return this._vueApp;
    }

    /**
     * The global ``WebComponent`` instance via Vue's injection mechanism.
     *
     * @throws Error - If no instance has been created.
     */
    public static injectComponent<CompType extends WebComponent = WebComponent>(): CompType {
        let inst = inject<CompType>(WebComponent._injectionKey);
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
