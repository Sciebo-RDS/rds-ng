import { SettingID } from "../utils/config/SettingID";
import { OAuth2AuthorizationSettingIDs } from "./AuthorizationSettingIDs";
import { GeneralSettingIDs } from "./GeneralSettingIDs";
import { NetworkClientSettingIDs } from "./NetworkSettingIDs";

/**
 * Gets default values for all settings.
 *
 * @returns - An object mapping the setting identifiers to their default values.
 */
export function getDefaultSettings(): Map<SettingID, any> {
    let defaults = new Map<SettingID, any>();

    // General settings
    defaults.set(GeneralSettingIDs.Debug, false);
    defaults.set(GeneralSettingIDs.NotificationTimeout, 3.0);

    // Network settings
    defaults.set(NetworkClientSettingIDs.ServerAddress, "");
    defaults.set(NetworkClientSettingIDs.ConnectionTimeout, 10);

    // Authorization settings
    defaults.set(OAuth2AuthorizationSettingIDs.ClientID, "");
    defaults.set(OAuth2AuthorizationSettingIDs.RedirectURL, "");

    return defaults;
}
