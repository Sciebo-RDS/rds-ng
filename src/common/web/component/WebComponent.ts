import { createPinia } from "pinia";
import BadgeDirective from "primevue/badgedirective";
import PrimeVue from "primevue/config";
import ConfirmDialog from "primevue/confirmdialog";
import ConfirmPopup from "primevue/confirmpopup";
import ConfirmationService from "primevue/confirmationservice";
import DynamicDialog from "primevue/dynamicdialog";
import DialogService from "primevue/dialogservice";
import Toast from "primevue/toast";
import ToastService from "primevue/toastservice";
import { type App, type Component as VueComp, createApp, inject } from "vue";
import { createRouter, createWebHistory, type Router, type RouteRecordRaw } from "vue-router";

import { Session } from "./Session";
import { WebComponentData } from "./WebComponentData";
import { Core } from "../core/Core";
import logging from "../core/logging/Logging";
import { registerAuthorizationStrategies } from "../integration/authorization/strategies/AuthorizationStrategies";
import { Service } from "../services/Service";
import { ServiceContext } from "../services/ServiceContext";
import { getDefaultSettings } from "../settings/DefaultSettings";
import { registerExporters } from "../ui/components/propertyeditor/exporters/Exporters";
import { UserInterface } from "../ui/UserInterface";
import { Configuration, type SettingsContainer } from "../utils/config/Configuration";
import { type Constructable } from "../utils/Types";
import { UnitID } from "../utils/UnitID";
import { MetaInformation } from "./MetaInformation";

import createComponentService from "../services/ComponentService";
import createNetworkService from "../services/NetworkService";
import createWebService from "../services/WebService";

import MainContainer from "../ui/views/main/MainViewContainer.vue";

// Load various icons
import "material-icons/css/material-icons.css";
import "material-icons/iconfont/outlined.css";
import "primeicons/primeicons.css";

// Necessary to make the entire API known
import "../api/API";

/**
 * Introduce a global type for Vue components.
 */
export type VueComponent = VueComp;

/**
 * Base class for all web components.
 *
 * By default, an instance of ``UserInterfaceType`` is used to create the main UI handler. This can be overriden using the corresponding
 * template and constructor parameters.
 *
 * Web applications are always based on this class. It mainly maintains an instance of the ``Core``, but also stores general information
 * about the application itself and the entire project.
 */
export class WebComponent<UserInterfaceType extends UserInterface = UserInterface> {
    private static _instance: WebComponent<any> | null = null;
    private static readonly _injectionKey = Symbol();

    protected readonly _session: Session;
    protected readonly _data: WebComponentData;

    protected readonly _core: Core;
    protected readonly _router: Router;

    protected readonly _userInterface: UserInterfaceType;
    protected readonly _vueApp: App;

    /**
     * @param env - The global environment variables.
     * @param compID - The identifier of this component.
     * @param appRoot - The root (main) application component.
     * @param userInterfaceType - The type of the user interface class.
     */
    public constructor(
        env: SettingsContainer,
        compID: UnitID,
        appRoot: VueComponent,
        userInterfaceType: Constructable<UserInterfaceType> = UserInterface as Constructable<UserInterfaceType>,
    ) {
        if (WebComponent._instance) {
            throw new Error("A component instance has already been created");
        }
        WebComponent._instance = this;

        const config = this.createConfig(env);
        const metaInfo = new MetaInformation();
        const compInfo = metaInfo.getComponent(compID.unit);

        this._session = new Session(compID);
        this._data = new WebComponentData(this.sanitizeComponentID(compID), config, metaInfo.title, compInfo.name, metaInfo.version);

        logging.info(this.toString());
        logging.info("Starting component");

        this._core = new Core(this._data);
        this._router = this.createRouter();

        this._userInterface = this.createUserInterface(userInterfaceType, appRoot);
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

    private createUserInterface(userInterfaceType: Constructable<UserInterfaceType>, appRoot: VueComponent): UserInterfaceType {
        return new userInterfaceType(this._router, appRoot);
    }

    private createVueApp(): App {
        logging.info("Creating Vue application");

        const app = createApp(MainContainer);

        // Register some global components
        app.component("ConfirmDialog", ConfirmDialog);
        app.component("ConfirmPopup", ConfirmPopup);
        app.component("DynamicDialog", DynamicDialog);
        app.component("Toast", Toast);

        // And some directives
        app.directive("badge", BadgeDirective);

        // Register various plugins
        app.use(createPinia());
        app.use(this._router);
        app.use(PrimeVue);
        app.use(ConfirmationService);
        app.use(DialogService);
        app.use(ToastService);

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
        logging.info("Running component");

        // Reigster global items
        registerAuthorizationStrategies();
        registerExporters();

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
    public createService<CtxType extends ServiceContext>(
        name: string,
        initializer: ((svc: Service) => void) | null = null,
        contextType: Constructable<CtxType> = ServiceContext as Constructable<CtxType>,
    ): Service {
        let svc = new Service<CtxType>(this._data.compID, name, this._core.messageBus, contextType);
        this._core.registerService(svc);
        if (initializer) {
            initializer(svc);
        }
        return svc;
    }

    /**
     * The client session.
     */
    public get session(): Session {
        return this._session;
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
     * The global user interface.
     */
    public get userInterface(): UserInterfaceType {
        return this._userInterface;
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
        const instance: string = compID.instance ? compID.instance : "default";
        return new UnitID(compID.type, compID.unit, `${instance}::${this.session.sessionID}`);
    }

    /**
     * @returns - The string representation of this component.
     */
    public toString(): string {
        return `${this._data.title} v${this._data.version}: ${this._data.name} (${this._data.compID})`;
    }
}
