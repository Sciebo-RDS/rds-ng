import { ComponentType, ComponentUnit } from "@common/component/ComponentIDs";
import { WebComponent } from "@common/component/WebComponent";
import { debug, error } from "@common/core/logging/Logging";
import { Service } from "@common/services/Service";
import { UnitID } from "@common/utils/UnitID";

import createFrontendService from "@/services/FrontendService";
import createUserService from "@/services/UserService";
import createConnectorsService from "@/services/ConnectorsService";
import createProjectsService from "@/services/ProjectsService";

import { getFrontendSettings } from "@/settings/FrontendSettings";
import { FrontendSettingIDs } from "@/settings/FrontendSettingIDs";

import Frontend from "@/ui/Frontend.vue";
import { FrontendUserInterface } from "@/ui/FrontendUserInterface";
import { AuthenticationScheme } from "@/authentication/AuthenticationScheme";
import { registerAuthenticationSchemes } from "@/authentication/AuthenticationSchemes";
import { AuthenticationSchemesCatalog } from "@/authentication/AuthenticationSchemesCatalog";
import { registerSnapIns } from "@/ui/snapins/SnapIns";

/**
 * The main frontend component class.
 */
export class FrontendComponent extends WebComponent<FrontendUserInterface> {
    private _authenticationScheme: AuthenticationScheme | null = null;

    private _frontendService: Service | null = null;
    private _userService: Service | null = null;
    private _connectorsService: Service | null = null;
    private _projectsService: Service | null = null;

    public constructor() {
        super(import.meta.env, new UnitID(ComponentType.Web, ComponentUnit.Frontend), Frontend, FrontendUserInterface);

        this.addFrontendSettings();
    }

    public run(): void {
        super.run();

        // Reigster global items
        registerAuthenticationSchemes();
        registerSnapIns();

        // Mount the authentication scheme
        this.mountAuthenticationScheme();

        // Create frontend-specific services
        this._frontendService = createFrontendService(this);
        this._userService = createUserService(this);
        this._connectorsService = createConnectorsService(this);
        this._projectsService = createProjectsService(this);
    }

    private addFrontendSettings(): void {
        this.data.config.addDefaults(getFrontendSettings());
    }

    private mountAuthenticationScheme(): void {
        const scheme = this._data.config.value<string>(FrontendSettingIDs.AuthenticationScheme);
        if (!scheme) {
            error("No authentication theme has been configured");
            return;
        }

        const authScheme = AuthenticationSchemesCatalog.findItem(scheme);
        if (!authScheme) {
            error(`The authentication scheme '${scheme}' couldn't be found`);
            return;
        }

        this._authenticationScheme = new authScheme(this);

        debug(`Using authentication scheme: ${scheme}`, "frontend");
    }

    /**
     * The active authentication scheme.
     */
    public get authenticationScheme(): AuthenticationScheme {
        if (!this._authenticationScheme) {
            throw new Error("Tried to access the authentication scheme before its creation");
        }
        return this._authenticationScheme;
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
     * The global ``FrontendComponent`` instance via Vue's injection mechanism.
     *
     * @throws Error - If no instance has been created.
     */
    public static inject(): FrontendComponent {
        return super.injectComponent<FrontendComponent>();
    }
}
