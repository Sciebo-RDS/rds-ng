/**
 * A token identifying a user within a host system.
 */
export interface HostUserToken {
    userID: string;
    userName: string;

    systemID: string;
    accessID: string;
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
        userName: data["user-name"],
        systemID: data["system-id"],
        accessID: data["access-id"],
    } as HostUserToken;
}

/**
 * Details about the host resources scheme.
 */
export interface HostResources {
    broker: string;
    config: Record<string, any>;
}
