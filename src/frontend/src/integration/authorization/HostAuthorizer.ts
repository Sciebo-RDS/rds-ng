import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import { createAuthorizationStrategy } from "@common/integration/authorization/strategies/AuthorizationStrategies";
import { type OAuth2Configuration, OAuth2Strategy } from "@common/integration/authorization/strategies/oauth2/OAuth2Strategy";

import { FrontendComponent } from "@/component/FrontendComponent";
import { Authorizer } from "@/integration/authorization/Authorizer";
import { type HostAuthorization } from "@/integration/HostTypes";
import { OAuth2AuthorizationSettingIDs } from "@/settings/AuthorizationSettingIDs";
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

    public authorize(authState: AuthorizationState, fingerprint: string): void {
        try {
            const strategy = createAuthorizationStrategy(
                this._component,
                this._component.frontendService,
                this._hostAuth.strategy,
                this.getStrategyConfiguration(this._hostAuth.strategy),
            );
            strategy
                .requestAuthorization(authState, fingerprint)
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

    private getStrategyConfiguration(strategy: string): Record<string, any> {
        switch (strategy) {
            case OAuth2Strategy.Strategy:
                return {
                    server: {
                        host: this._hostAuth.config.host || "",
                        endpoints: {
                            authorization: this._hostAuth.config.endpoints?.authorization || "",
                            token: this._hostAuth.config.endpoints?.token || "",
                        },
                    },
                    client: {
                        clientID: this._component.data.config.value<string>(OAuth2AuthorizationSettingIDs.ClientID),
                        redirectURL: this._component.data.config.value<string>(OAuth2AuthorizationSettingIDs.RedirectURL),
                        embedded: this._component.data.config.value<boolean>(HostIntegrationSettingIDs.Embedded),
                    },
                } as OAuth2Configuration;

            default:
                return {};
        }
    }
}
