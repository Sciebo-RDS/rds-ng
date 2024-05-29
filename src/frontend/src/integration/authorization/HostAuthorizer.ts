import { FrontendComponent } from "@/component/FrontendComponent";

import { Authorizer } from "@/integration/authorization/Authorizer";
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
            // Use strategy
            this.setAuthorized(true);
        } catch (exc) {
            this.setAuthorized(false, `Authorization failed: ${exc}`);
        }
    }
}
