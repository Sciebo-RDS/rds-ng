import { type UserID } from "../user/User";

export type AuthorizationTokenID = [UserID, string];

/**
 * Various authorization token types.
 */
export const enum AuthorizationTokenType {
    Host = "host",
    Connector = "connector",
}
