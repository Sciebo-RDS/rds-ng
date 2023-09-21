import { ComponentType, ComponentUnit } from "@common/component/ComponentIDs";
import { WebComponent } from "@common/component/WebComponent";
import type { Service } from "@common/services/Service";
import { UnitID } from "@common/utils/UnitID";

import createFrontendService from "@/services/FrontendService";

import Frontend from "@/ui/Frontend.vue";

/**
 * The main frontend component class.
 */
export class FrontendComponent extends WebComponent {
    private _frontendService: Service | null = null;

    public constructor() {
        super(import.meta.env, new UnitID(ComponentType.Web, ComponentUnit.Frontend), Frontend);
    }

    public run(): void {
        super.run();

        // Create frontend-specific services
        this._frontendService = createFrontendService(this);
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

    public static inject(): FrontendComponent {
        return super.injectComponent<FrontendComponent>();
    }
}
