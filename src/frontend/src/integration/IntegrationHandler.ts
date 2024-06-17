import type { FrontendComponent } from "@/component/FrontendComponent";

/**
 * Base class for all integration handlers.
 */
export abstract class IntegrationHandler {
    protected readonly _component: FrontendComponent;

    protected constructor(comp: FrontendComponent) {
        this._component = comp;
    }
}
