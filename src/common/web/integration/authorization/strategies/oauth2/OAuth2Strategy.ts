import { WebComponent } from "../../../../component/WebComponent";
import { Service } from "../../../../services/Service";
import { RedirectionTarget } from "../../../../utils/HTMLUtils";
import { getURLQueryParam } from "../../../../utils/URLUtils";
import { AuthorizationRequest } from "../../AuthorizationRequest";
import { AuthorizationStrategy } from "../AuthorizationStrategy";
import { type OAuth2AuthorizationRequestData } from "./OAuth2Types";

/**
 * The OAuth2 strategy configuration.
 */
export interface OAuth2StrategyConfiguration {
    server: {
        host: string;
        authorization_endpoint: string;
        token_endpoint: string;
        scope: string;
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

    protected initiateRequest(authRequest: AuthorizationRequest): void {
        const url = new URL(this._config.server.authorization_endpoint, new URL(this._config.server.host));
        url.searchParams.set("response_type", "code");
        url.searchParams.set("client_id", this._config.client.client_id);
        url.searchParams.set("scope", this._config.server.scope);
        url.searchParams.set("access_type", "offline");
        url.searchParams.set("approval_prompt", "auto");
        url.searchParams.set("redirect_uri", this._config.client.redirect_url);
        url.searchParams.set("state", authRequest.encodedPayload);
        this.redirect(url.toString());
    }

    protected getRequestData(_: AuthorizationRequest): any {
        const authCode = getURLQueryParam("auth:code");
        if (!authCode) {
            throw new Error("No authentication code provided");
        }

        return {
            token_host: this._config.server.host,
            token_endpoint: this._config.server.token_endpoint,

            client_id: this._config.client.client_id,
            auth_code: authCode,
            scope: this._config.server.scope,

            redirect_url: this._config.client.redirect_url,
        } as OAuth2AuthorizationRequestData;
    }

    protected finishRequest(): void {
        if (this._redirectionTarget == RedirectionTarget.Blank) {
            // Even if there's no parent, this will work
            window.parent.close();
        } else {
            this.redirect(this._config.client.redirect_url);
        }
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
    if (!oauth2Config.server?.authorization_endpoint) {
        throw new Error("Missing authorization endpoint");
    }
    if (!oauth2Config.server?.token_endpoint) {
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
