import { FrontendComponent } from "@/component/FrontendComponent";
import { IntegrationPerformer } from "@/integration/IntegrationPerformer";

export class Authorizer extends IntegrationPerformer {
    public constructor(comp: FrontendComponent) {
        super(comp);
    }

    /**
     * Authorize the integration.
     */
    public authorize(): void {}
}
