import { FrontendComponent } from "@/component/FrontendComponent";
import { createAuthorizationStrategy } from "@common/integration/authorization/AuthorizationStrategies";
import { AuthorizationStrategy } from "@common/integration/authorization/AuthorizationStrategy";

import { Authorizer } from "@/integration/auth/Authorizer";
import { type HostAuthorization } from "@/integration/HostTypes";
import { HostIntegrationSettingIDs } from "@/settings/IntegrationSettingIDs";

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
            const authStrategy = this.createStrategy();

            authStrategy.requestAuthorization(); // Will throw an exception upon failure
            this.setAuthorized(true);
        } catch (exc) {
            this.setAuthorized(false, `Authorization failed: ${exc}`);
        }
    }

    private createStrategy(): AuthorizationStrategy {
        const strategy = this._hostAuth.strategy;
        if (!strategy) {
            throw new Error("No authorization strategy has been configured");
        }

        return createAuthorizationStrategy(
            this._component,
            strategy,
            this._hostAuth.config,
            this._component.data.config.value<boolean>(HostIntegrationSettingIDs.Embedded),
        );
    }
}
