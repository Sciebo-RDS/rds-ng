import { RedirectionTarget } from "../../../../utils/HTMLUtils";

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
 * OAuth2 authorization request data.
 */
export interface OAuth2AuthorizationRequestData {
    token_host: string;
    token_endpoint: string;

    client_id: string;
    auth_code: string;
    scope: string;

    redirect_url: string;
}
