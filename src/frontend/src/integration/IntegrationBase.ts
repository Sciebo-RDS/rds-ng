import type { FrontendComponent } from "@/component/FrontendComponent";

/**
 * Base class for all integration parts.
 */
export abstract class IntegrationBase {
    protected readonly _component: FrontendComponent;

    protected constructor(comp: FrontendComponent) {
        this._component = comp;
    }
}
