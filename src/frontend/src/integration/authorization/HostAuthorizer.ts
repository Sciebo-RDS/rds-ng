import { FrontendComponent } from "@/component/FrontendComponent";
import { Authorizer } from "@/integration/authorization/Authorizer";
import { OAuth2AuthorizationSettingIDs } from "@/settings/AuthorizationSettingIDs";
import { HostIntegrationSettingIDs } from "@/settings/IntegrationSettingIDs";
import { type AuthorizationSettings } from "@common/data/entities/authorization/AuthorizationSettings";
import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import { AuthorizationTokenType } from "@common/data/entities/authorization/AuthorizationToken";
import { createAuthorizationStrategy } from "@common/integration/authorization/strategies/AuthorizationStrategies";
import { OAuth2Strategy, type OAuth2StrategyConfiguration } from "@common/integration/authorization/strategies/oauth2/OAuth2Strategy";
import { RedirectionTarget } from "@common/utils/HTMLUtils";

/**
 * Authorizer for host integration.
 */
export class HostAuthorizer extends Authorizer {
    private readonly _hostAuth: AuthorizationSettings;

    public constructor(comp: FrontendComponent, hostAuth: AuthorizationSettings) {
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
                .requestAuthorization(AuthorizationTokenType.Host, AuthorizationTokenType.Host, AuthorizationTokenType.Host, authState, fingerprint)
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
                        client_id: this._component.data.config.value<string>(OAuth2AuthorizationSettingIDs.ClientID),
                        redirect_url: this._component.data.config.value<string>(OAuth2AuthorizationSettingIDs.RedirectURL),
                        redirect_target: this._component.data.config.value<boolean>(HostIntegrationSettingIDs.Embedded)
                            ? RedirectionTarget.Parent
                            : RedirectionTarget.Same,
                    },
                } as OAuth2StrategyConfiguration;

            default:
                return {};
        }
    }
}
