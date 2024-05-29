import { FrontendComponent } from "@/component/FrontendComponent";
import { Authorizer } from "@/integration/authorization/Authorizer";

/**
 * Authorizer for basic integration.
 */
export class BasicAuthorizer extends Authorizer {
    public constructor(comp: FrontendComponent) {
        super(comp);
    }

    public authorize(): void {
        // Basic authorization simply skips actual authorization
        this.setAuthorized(true);
    }
}
