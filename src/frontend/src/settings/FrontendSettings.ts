import { SettingID } from "@common/utils/config/SettingID";

import { FrontendSettingIDs } from "@/settings/FrontendSettingIDs";
import { HostIntegrationSettingIDs, IntegrationSettingIDS } from "@/settings/IntegrationSettingIDs";

/**
 * Gets default values for all frontend settings.
 *
 * @returns - An object mapping the setting identifiers to their default values.
 */
export function getFrontendSettings(): Map<SettingID, any> {
    let settings = new Map<SettingID, any>();

    // Frontend settings
    settings.set(FrontendSettingIDs.RegularCommandTimeout, 10.0);

    // Integration settings
    settings.set(IntegrationSettingIDS.Scheme, "basic");

    settings.set(HostIntegrationSettingIDs.APIURL, "");
    settings.set(HostIntegrationSettingIDs.Embedded, true);

    return settings;
}
