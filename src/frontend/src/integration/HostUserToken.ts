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
 * @param tokenData - The JSON data.
 *
 * @returns - The host user token.
 */
export function hostUserTokenFromData(tokenData: Record<string, any>): HostUserToken {
    return {
        userID: tokenData["user-id"],
        systemID: tokenData["system-id"],
        userName: tokenData["user-name"],
    } as HostUserToken;
}
