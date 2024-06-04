import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import { getURLQueryParam } from "@common/utils/URLUtils";

import { FrontendComponent } from "@/component/FrontendComponent";
import { AuthorizationStrategy } from "@/integration/authorization/strategies/AuthorizationStrategy";
import { OAuth2AuthorizationSettingIDs } from "@/settings/AuthorizationSettingIDs";
import { HostIntegrationSettingIDs } from "@/settings/IntegrationSettingIDs";

/**
 * The OAuth2 strategy configuration.
 */
export interface OAuth2Configuration {
    server: {
        endpoints: {
            authorization: string;
            token: string;
        };
    };
    client: {
        clientID: string;
        redirectURL: string;
        embedded: boolean;
    };
}

/**
 * OAuth2 authorization request data.
 */
export interface OAuth2AuthorizationRequestData {
    auth: {
        code: string;
    };
    endpoints: {
        token: string;
    };
}

/**
 * OAuth2 authorization strategy.
 */
export class OAuth2Strategy extends AuthorizationStrategy {
    public static readonly Strategy = "oauth2";

    private readonly _config: OAuth2Configuration;

    public constructor(comp: FrontendComponent, config: OAuth2Configuration) {
        super(comp, OAuth2Strategy.Strategy, config.client.embedded);

        this.verifyConfiguration(config);
        this._config = config;
    }

    protected initiateRequest(): void {
        this.redirect(this.getAuthorizationURL());
    }

    protected getRequestData(): any {
        const authCode = getURLQueryParam("auth:code");
        if (!authCode) {
            throw new Error("No authentication code provided");
        }

        return {
            auth: {
                code: authCode,
            },
            endpoints: {
                token: this._config.server.endpoints.token,
            },
        } as OAuth2AuthorizationRequestData;
    }

    protected finishRequest(authState: AuthorizationState): void {
        if (authState == AuthorizationState.Authorized) {
            this.redirect(this._config.client.redirectURL);
        }
    }

    private verifyConfiguration(config: OAuth2Configuration): void {
        // Server configuration
        if (!config.server.endpoints.authorization) {
            throw new Error("Missing authorization endpoint");
        }
        if (!config.server.endpoints.token) {
            throw new Error("Missing token endpoint");
        }

        // Client configuration
        if (!config.client.clientID) {
            throw new Error("Missing client ID");
        }
        if (!config.client.redirectURL) {
            throw new Error("Missing redirection URL");
        }
    }

    private getAuthorizationURL(): string {
        const url = new URL(this._config.server.endpoints.authorization);
        url.searchParams.set("response_type", "code");
        url.searchParams.set("client_id", this._config.client.clientID);
        url.searchParams.set("redirect_uri", this._config.client.redirectURL);
        url.searchParams.set("state", "code"); // TODO: Dynamic (from backend)
        return url.toString();
    }
}

/**
 * Creates a new OAuth2 strategy instance, automatically configuring it.
 *
 * @param comp - The main component.
 * @param config - The host strategy configuration as an arbitrary record.
 *
 * @returns - The newly created strategy.
 */
export function createOAuth2Strategy(comp: FrontendComponent, config: Record<string, any>): OAuth2Strategy {
    const oauth2Config = {
        server: {
            endpoints: {
                authorization: config.endpoints.authorization || "",
                token: config.endpoints.token || "",
            },
        },
        client: {
            clientID: comp.data.config.value<string>(OAuth2AuthorizationSettingIDs.ClientID),
            redirectURL: comp.data.config.value<string>(OAuth2AuthorizationSettingIDs.RedirectURL),
            embedded: comp.data.config.value<boolean>(HostIntegrationSettingIDs.Embedded),
        },
    } as OAuth2Configuration;

    return new OAuth2Strategy(comp, oauth2Config);
}
