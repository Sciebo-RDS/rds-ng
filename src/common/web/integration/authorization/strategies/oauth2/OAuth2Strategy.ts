import { WebComponent } from "../../../../component/WebComponent";
import { AuthorizationState } from "../../../../data/entities/authorization/AuthorizationState";
import { Service } from "../../../../services/Service";
import { getURLQueryParam } from "../../../../utils/URLUtils";
import { AuthorizationStrategy } from "../AuthorizationStrategy";
import { type OAuth2AuthorizationRequestData } from "./OAuth2Types";

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
 * OAuth2 authorization strategy.
 */
export class OAuth2Strategy extends AuthorizationStrategy {
    public static readonly Strategy = "oauth2";

    private readonly _config: OAuth2Configuration;

    public constructor(comp: WebComponent, svc: Service, config: OAuth2Configuration) {
        super(comp, svc, OAuth2Strategy.Strategy, config.client.embedded);

        this._config = config;
    }

    protected initiateRequest(fingerprint: string): void {
        const url = new URL(this._config.server.endpoints.authorization);
        url.searchParams.set("response_type", "code");
        url.searchParams.set("client_id", this._config.client.clientID);
        url.searchParams.set("redirect_uri", this._config.client.redirectURL);
        url.searchParams.set("state", fingerprint);
        this.redirect(url.toString());
    }

    protected getRequestData(): any {
        const authCode = getURLQueryParam("auth:code");
        if (!authCode) {
            throw new Error("No authentication code provided");
        }

        return {
            token_endpoint: this._config.server.endpoints.token,

            client_id: this._config.client.clientID,
            auth_code: authCode,

            redirect_url: this._config.client.redirectURL,
        } as OAuth2AuthorizationRequestData;
    }

    protected finishRequest(authState: AuthorizationState): void {
        if (authState == AuthorizationState.Authorized) {
            this.redirect(this._config.client.redirectURL);
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
    const oauth2Config = config as OAuth2Configuration;

    // Verify the passed configuration
    if (!oauth2Config.server?.endpoints?.authorization) {
        throw new Error("Missing authorization endpoint");
    }
    if (!oauth2Config.server?.endpoints?.token) {
        throw new Error("Missing token endpoint");
    }

    if (!oauth2Config.client?.clientID) {
        throw new Error("Missing client ID");
    }
    if (!oauth2Config.client?.redirectURL) {
        throw new Error("Missing redirection URL");
    }

    return new OAuth2Strategy(comp, svc, oauth2Config);
}
