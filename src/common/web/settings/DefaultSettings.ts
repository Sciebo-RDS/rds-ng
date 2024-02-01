import { SettingID } from "../utils/config/SettingID";
import { GeneralSettingIDs } from "./GeneralSettingIDs";
import { NetworkClientSettingIDs } from "./NetworkSettingIDs";

/**
 * Gets default values for all settings.
 *
 * @returns - An object mapping the setting identifiers to their default values.
 */
export function getDefaultSettings(): Map<SettingID, any> {
    let defaults = new Map<SettingID, any>();

    defaults.set(GeneralSettingIDs.Debug, false);
    defaults.set(GeneralSettingIDs.SessionKey, "session-id");
    defaults.set(GeneralSettingIDs.NotificationTimeout, 3.0);

    defaults.set(NetworkClientSettingIDs.ServerAddress, "");
    defaults.set(NetworkClientSettingIDs.ConnectionTimeout, 10);

    return defaults;
}
