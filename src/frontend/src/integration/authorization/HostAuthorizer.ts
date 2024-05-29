import { FrontendComponent } from "@/component/FrontendComponent";

import { Authorizer } from "@/integration/authorization/Authorizer";
import { createAuthorizationStrategy } from "@/integration/authorization/strategies/AuthorizationStrategies";
import { type HostAuthorization } from "@/integration/HostTypes";

/**
 * Authorizer for host integration.
 */
export class HostAuthorizer extends Authorizer {
    private readonly _hostAuth: HostAuthorization;

    public constructor(comp: FrontendComponent, hostAuth: HostAuthorization) {
        super(comp);

        this._hostAuth = hostAuth;
    }

    public authorize(): void {
        try {
            const strategy = createAuthorizationStrategy(this._component, this._hostAuth.strategy, this._hostAuth.config);
            strategy.requestAuthorization();
            this.setAuthorized(true);
        } catch (exc) {
            this.setAuthorized(false, `Authorization failed: ${exc}`);
        }
    }
}
