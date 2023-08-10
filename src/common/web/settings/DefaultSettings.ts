import { GeneralSettingIDs } from "./GeneralSettingIDs";
import { NetworkSettingIDs } from "./NetworkSettingIDs";
import { SettingID } from "../utils/config/SettingID";

/**
 * Gets default values for all settings.
 *
 * @returns - An object mapping the setting identifiers to their default values.
 */
export function getDefaultSettings(): Map<SettingID, any> {
    let defaults = new Map<SettingID, any>();

    defaults.set(GeneralSettingIDs.Debug, false);

    defaults.set(NetworkSettingIDs.ServerAddress, "");
    defaults.set(NetworkSettingIDs.ConnectionTimeout, 10);

    return defaults;
}
