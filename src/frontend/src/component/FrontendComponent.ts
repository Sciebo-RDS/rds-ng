import { ComponentType, ComponentUnit } from "@common/component/ComponentIDs";
import { WebComponent } from "@common/component/WebComponent";
import { debug, error } from "@common/core/logging/Logging";
import { Service } from "@common/services/Service";
import { UnitID } from "@common/utils/UnitID";

import { registerConnectorCategories } from "@/data/entities/connector/categories/ConnectorCategories";

import { IntegrationScheme } from "@/integration/IntegrationScheme";
import { registerIntegrationSchemes } from "@/integration/IntegrationSchemes";
import { IntegrationSchemesCatalog } from "@/integration/IntegrationSchemesCatalog";

import createConnectorsService from "@/services/ConnectorsService";
import createFrontendService from "@/services/FrontendService";
import createProjectsService from "@/services/ProjectsService";
import createProjectJobsService from "@/services/ProjectJobsService";
import createUserService from "@/services/UserService";

import { getFrontendSettings } from "@/settings/FrontendSettings";
import { IntegrationSettingIDS } from "@/settings/IntegrationSettingIDs";

import Frontend from "@/ui/Frontend.vue";
import { FrontendUserInterface } from "@/ui/FrontendUserInterface";
import { registerSnapIns } from "@/ui/snapins/SnapIns";

/**
 * The main frontend component class.
 */
export class FrontendComponent extends WebComponent<FrontendUserInterface> {
    private _integrationScheme: IntegrationScheme | null = null;

    private _frontendService: Service | null = null;
    private _userService: Service | null = null;
    private _connectorsService: Service | null = null;
    private _projectsService: Service | null = null;
    private _projectJobsService: Service | null = null;

    public constructor() {
        super(import.meta.env, new UnitID(ComponentType.Web, ComponentUnit.Frontend), Frontend, FrontendUserInterface);

        this.addFrontendSettings();
    }

    public run(): void {
        super.run();

        // Reigster global items
        registerIntegrationSchemes();
        registerConnectorCategories();
        registerSnapIns();

        // Mount the integration scheme
        this.mountIntegrationScheme();

        // Create frontend-specific services
        this._frontendService = createFrontendService(this);
        this._userService = createUserService(this);
        this._connectorsService = createConnectorsService(this);
        this._projectsService = createProjectsService(this);
        this._projectJobsService = createProjectJobsService(this);
    }

    private addFrontendSettings(): void {
        this.data.config.addDefaults(getFrontendSettings());
    }

    private mountIntegrationScheme(): void {
        const scheme = this._data.config.value<string>(IntegrationSettingIDS.Scheme);
        if (!scheme) {
            error("No integration scheme has been configured");
            return;
        }

        const intScheme = IntegrationSchemesCatalog.findItem(scheme);
        if (!intScheme) {
            error(`The integration scheme '${scheme}' couldn't be found`);
            return;
        }

        this._integrationScheme = new intScheme(this);

        debug(`Using integration scheme: ${scheme}`, "frontend");
    }

    /**
     * The active integration scheme.
     */
    public get integrationScheme(): IntegrationScheme {
        if (!this._integrationScheme) {
            throw new Error("Tried to access the integration scheme before its creation");
        }
        return this._integrationScheme;
    }

    /**
     * The main frontend service.
     */
    public get frontendService(): Service {
        if (!this._frontendService) {
            throw new Error("Tried to access the frontend service before its creation");
        }
        return this._frontendService;
    }

    /**
     * The user service.
     */
    public get userService(): Service {
        if (!this._userService) {
            throw new Error("Tried to access the user service before its creation");
        }
        return this._userService;
    }

    /**
     * The connectors service.
     */
    public get connectorsService(): Service {
        if (!this._connectorsService) {
            throw new Error("Tried to access the connectors service before its creation");
        }
        return this._connectorsService;
    }

    /**
     * The projects service.
     */
    public get projectsService(): Service {
        if (!this._projectsService) {
            throw new Error("Tried to access the projects service before its creation");
        }
        return this._projectsService;
    }

    /**
     * The project jobs service.
     */
    public get projectJobsService(): Service {
        if (!this._projectJobsService) {
            throw new Error("Tried to access the jobs service before its creation");
        }
        return this._projectJobsService;
    }

    /**
     * The global ``FrontendComponent`` instance via Vue's injection mechanism.
     *
     * @throws Error - If no instance has been created.
     */
    public static inject(): FrontendComponent {
        return super.injectComponent<FrontendComponent>();
    }
}
