import { SettingID } from "@common/utils/config/SettingID";

/**
 * Identifiers for general authorization settings.
 */
export class AuthorizationSettingIDs {}

/**
 * Identifiers for OAuth2 authorization.
 *
 * @property ClientID - The client ID (value type: ``string``).
 * @property RedirectURL - The redirection URL (value type: ``string``).
 */
export class OAuth2AuthorizationSettingIDs {
    public static readonly ClientID = new SettingID("authorization.oauth2", "client.id");
    public static readonly RedirectURL = new SettingID("authorization.oauth2", "client.redirect_url");
}
