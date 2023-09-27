import { ComponentType, ComponentUnit } from "@common/component/ComponentIDs";
import { WebComponent } from "@common/component/WebComponent";
import { Service } from "@common/services/Service";
import { UnitID } from "@common/utils/UnitID";

import { getFrontendSettings } from "@/settings/FrontendSettings";

import createFrontendService from "@/services/FrontendService";
import createProjectsService from "@/services/ProjectsService";

import Frontend from "@/ui/Frontend.vue";

/**
 * The main frontend component class.
 */
export class FrontendComponent extends WebComponent {
    private _frontendService: Service | null = null;
    private _projectsService: Service | null = null;

    public constructor() {
        super(import.meta.env, new UnitID(ComponentType.Web, ComponentUnit.Frontend), Frontend);

        this.addFrontendSettings();
    }

    public run(): void {
        super.run();

        // Create frontend-specific services
        this._frontendService = createFrontendService(this);
        this._projectsService = createProjectsService(this);
    }

    private addFrontendSettings(): void {
        this.data.config.addDefaults(getFrontendSettings());
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
     * The projects service.
     */
    public get projectsService(): Service {
        if (!this._projectsService) {
            throw new Error("Tried to access the projects service before its creation");
        }
        return this._projectsService;
    }

    public static inject(): FrontendComponent {
        return super.injectComponent<FrontendComponent>();
    }
}
