import { WebComponent } from "../../../../component/WebComponent";
import { Service } from "../../../../services/Service";
import { RedirectionTarget } from "../../../../utils/HTMLUtils";
import { getURLQueryParam } from "../../../../utils/URLUtils";
import { AuthorizationStrategy } from "../AuthorizationStrategy";
import { type OAuth2AuthorizationRequestData } from "./OAuth2Types";

/**
 * The OAuth2 strategy configuration.
 */
export interface OAuth2StrategyConfiguration {
    server: {
        host: string;
        endpoints: {
            authorization: string;
            token: string;
        };
    };
    client: {
        client_id: string;
        redirect_url: string;
        redirect_target: RedirectionTarget;
    };
}

/**
 * OAuth2 authorization strategy.
 */
export class OAuth2Strategy extends AuthorizationStrategy {
    public static readonly Strategy = "oauth2";

    private readonly _config: OAuth2StrategyConfiguration;

    public constructor(comp: WebComponent, svc: Service, config: OAuth2StrategyConfiguration) {
        super(comp, svc, OAuth2Strategy.Strategy, config.client.redirect_target);

        this._config = config;
    }

    protected initiateRequest(payload: string): void {
        const url = new URL(this._config.server.endpoints.authorization, new URL(this._config.server.host));
        url.searchParams.set("response_type", "code");
        url.searchParams.set("client_id", this._config.client.client_id);
        url.searchParams.set("redirect_uri", this._config.client.redirect_url);
        url.searchParams.set("state", payload);
        this.redirect(url.toString());
    }

    protected getRequestData(): any {
        const authCode = getURLQueryParam("auth:code");
        if (!authCode) {
            throw new Error("No authentication code provided");
        }

        return {
            token_host: this._config.server.host,
            token_endpoint: this._config.server.endpoints.token,

            client_id: this._config.client.client_id,
            auth_code: authCode,

            redirect_url: this._config.client.redirect_url,
        } as OAuth2AuthorizationRequestData;
    }

    protected finishRequest(): void {
        this.redirect(this._config.client.redirect_url);
    }
}

/**
 * Creates a new OAuth2 strategy instance, automatically configuring it.
 *
 * @param comp - The main component.
 * @param svc - The service to use for message sending.
 * @param config - The strategy configuration.
 *
 * @returns - The newly created strategy.
 */
export function createOAuth2Strategy(comp: WebComponent, svc: Service, config: Record<string, any>): OAuth2Strategy {
    const oauth2Config = config as OAuth2StrategyConfiguration;

    // Verify the passed configuration
    if (!oauth2Config.server?.host) {
        throw new Error("Missing authorization host");
    }
    if (!oauth2Config.server?.endpoints?.authorization) {
        throw new Error("Missing authorization endpoint");
    }
    if (!oauth2Config.server?.endpoints?.token) {
        throw new Error("Missing token endpoint");
    }

    if (!oauth2Config.client?.client_id) {
        throw new Error("Missing client ID");
    }
    if (!oauth2Config.client?.redirect_url) {
        throw new Error("Missing redirection URL");
    }

    return new OAuth2Strategy(comp, svc, oauth2Config);
}
