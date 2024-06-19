import { type UserID } from "../user/User";

export type AuthorizationTokenID = [UserID, string];

/**
 * Various authorization token types.
 */
export const enum AuthorizationTokenType {
    Invalid = "",

    Host = "host",
    Connector = "connector",
}

/**
 * Gets an array of all non-host token types.
 */
export function getNonHostTokenTypes(): AuthorizationTokenType[] {
    return [AuthorizationTokenType.Connector];
}
