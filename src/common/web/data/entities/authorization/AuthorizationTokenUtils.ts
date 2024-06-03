import { UserID } from "../user/User";
import { AuthorizationTokenID } from "./AuthorizationToken";

/**
 * Retrieves the authorization token ID for the user host system.
 *
 * @param userID - The user ID.
 *
 * @returns - The authorization token ID.
 */
export function getHostAuthorizationTokenID(userID: UserID): AuthorizationTokenID {
    return [userID, "host"];
}
