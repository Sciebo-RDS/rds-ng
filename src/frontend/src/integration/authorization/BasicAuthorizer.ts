import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";

import { FrontendComponent } from "@/component/FrontendComponent";
import { Authorizer } from "@/integration/authorization/Authorizer";

/**
 * Authorizer for basic integration.
 */
export class BasicAuthorizer extends Authorizer {
    public constructor(comp: FrontendComponent) {
        super(comp);
    }

    public authorize(_: AuthorizationState): void {
        // Basic authorization simply skips actual authorization
        this.setAuthorizationState(AuthorizationState.Authorized);
    }
}
