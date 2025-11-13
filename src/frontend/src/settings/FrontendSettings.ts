import { SettingID } from "@common/utils/config/SettingID";

/**
 * Gets default values for all frontend settings.
 *
 * @returns - An object mapping the setting identifiers to their default values.
 */
export function getFrontendSettings(): Map<SettingID, any> {
    return new Map<SettingID, any>();
}
