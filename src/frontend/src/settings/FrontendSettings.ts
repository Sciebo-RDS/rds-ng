import { SettingID } from "@common/utils/config/SettingID";

import { LoginType } from "@/integration/Login";
import { FrontendSettingIDs } from "@/settings/FrontendSettingIDs";

/**
 * Gets default values for all frontend settings.
 *
 * @returns - An object mapping the setting identifiers to their default values.
 */
export function getFrontendSettings(): Map<SettingID, any> {
    let settings = new Map<SettingID, any>();

    settings.set(FrontendSettingIDs.RegularCommandTimeout, 10.0);

    settings.set(FrontendSettingIDs.PublicKeyURL, "");

    settings.set(FrontendSettingIDs.LoginType, LoginType.Basic);

    return settings;
}
