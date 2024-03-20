/**
 * A token identifying the currently authenticated user.
 */
export interface UserToken {
    userID: string;
    userName: string;
}

/**
 * Creates a new user token.
 *
 * @param userID - The user ID.
 * @param userName - The username.
 */
export function createUserToken(userID: string, userName?: string): UserToken {
    return {
        userID: userID,
        userName: userName || userID
    } as UserToken;
}

/**
 * Checks whether a user token is valid.
 *
 * @param token - The user token.
 */
export function isUserTokenValid(token: UserToken): boolean {
    return !!token.userID;
}
