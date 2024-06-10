/**
 * Details about the host authorization scheme.
 */
export interface HostAuthorization {
    strategy: string;
    config: Record<string, any>;
}

/**
 * Converts an object (usually JSON) into a HostAuthorization.
 *
 * @param data - The JSON data.
 *
 * @returns - The host user token.
 */
export function hostAuthorizationFromData(data: Record<string, any>): HostAuthorization {
    return {
        strategy: data["strategy"],
        config: data["config"],
    } as HostAuthorization;
}

/**
 * A token identifying a user within a host system.
 */
export interface HostUserToken {
    userID: string;
    systemID: string;
    userName: string;
}

/**
 * Converts an object (usually JSON) into a HostUserToken.
 *
 * @param data - The JSON data.
 *
 * @returns - The host user token.
 */
export function hostUserTokenFromData(data: Record<string, any>): HostUserToken {
    return {
        userID: data["user-id"],
        systemID: data["system-id"],
        userName: data["user-name"],
    } as HostUserToken;
}
