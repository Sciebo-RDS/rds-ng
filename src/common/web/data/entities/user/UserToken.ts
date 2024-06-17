/**
 * A token identifying the currently authenticated user.
 */
export interface UserToken {
    user_id: string;
    user_name: string;

    system_id: string;
    access_id: string;
}

/**
 * Creates a new user token.
 *
 * @param userID - The user ID.
 * @param userName - The username.
 * @param systemID - The user's system-specific ID.
 * @param accessID - A well-formatted ID used to access resources.
 */
export function createUserToken(userID: string, userName?: string, systemID?: string, accessID?: string): UserToken {
    return {
        user_id: userID,
        user_name: userName || userID,
        system_id: systemID || userID,
        access_id: accessID || userID,
    } as UserToken;
}

/**
 * Checks whether a user token is valid.
 *
 * @param token - The user token.
 */
export function isUserTokenValid(token: UserToken): boolean {
    return !!token.user_id;
}
