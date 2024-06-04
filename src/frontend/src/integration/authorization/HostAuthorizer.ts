import { FrontendComponent } from "@/component/FrontendComponent";
import { Authorizer } from "@/integration/authorization/Authorizer";
import { createAuthorizationStrategy } from "@/integration/authorization/strategies/AuthorizationStrategies";
import { type HostAuthorization } from "@/integration/HostTypes";
import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";

/**
 * Authorizer for host integration.
 */
export class HostAuthorizer extends Authorizer {
    private readonly _hostAuth: HostAuthorization;

    public constructor(comp: FrontendComponent, hostAuth: HostAuthorization) {
        super(comp);

        this._hostAuth = hostAuth;
    }

    public authorize(authState: AuthorizationState): void {
        try {
            const strategy = createAuthorizationStrategy(this._component, this._hostAuth.strategy, this._hostAuth.config);
            strategy
                .requestAuthorization(authState)
                .then((authState: AuthorizationState) => {
                    // Skip any non-authorized states, as these will occur during the multistep authorization process
                    if (authState == AuthorizationState.Authorized) {
                        this.setAuthorizationState(AuthorizationState.Authorized);
                    }
                })
                .catch((err: Error) => {
                    this.setAuthorizationState(AuthorizationState.NotAuthorized, `Authorization failed: ${err}`);
                });
        } catch (exc) {
            this.setAuthorizationState(AuthorizationState.NotAuthorized, `Authorization failed: ${exc}`);
        }
    }
}
