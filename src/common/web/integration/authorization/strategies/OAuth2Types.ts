/**
 * OAuth2 authorization request data.
 */
export interface OAuth2AuthorizationRequestData {
    token_endpoint: string;

    client_id: string;
    auth_code: string;

    redirect_url: string;
}