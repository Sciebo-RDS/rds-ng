import { AuthorizationRequest } from "./AuthorizationRequest";

/**
 * Gets helpful logging parameters from an authorization request.
 *
 * @param authRequest - The authorization request.
 *
 * @returns - A dictionary with useful information.
 */
export function getAuthorizationRequestLoggingParams(authRequest: AuthorizationRequest): Record<string, any> {
    return {
        id: authRequest.payload.auth_id,
        type: authRequest.payload.auth_type,
        issuer: authRequest.payload.auth_issuer
    };
}
