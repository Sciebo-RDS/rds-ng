import { type UserID } from "../user/User";

export type AuthorizationTokenID = [UserID, string];

/**
 * Various authorization token types.
 */
export const enum AuthorizationTokenType {
    Host = "host",
    Connector = "connector",
}

/**
 * Gets an array of all non-host token types.
 */
export function getAllNonHostTokenTypes(): AuthorizationTokenType[] {
    return [AuthorizationTokenType.Connector];
}
