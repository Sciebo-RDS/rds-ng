import { SettingID } from "@common/utils/config/SettingID";

import { OAuth2AuthorizationSettingIDs } from "@/settings/AuthorizationSettingIDs";
import { HostIntegrationSettingIDs, IntegrationSettingIDS } from "@/settings/IntegrationSettingIDs";

/**
 * Gets default values for all frontend settings.
 *
 * @returns - An object mapping the setting identifiers to their default values.
 */
export function getFrontendSettings(): Map<SettingID, any> {
    let settings = new Map<SettingID, any>();

    // Integration settings
    settings.set(IntegrationSettingIDS.Scheme, "basic");

    settings.set(HostIntegrationSettingIDs.APIURL, "");
    settings.set(HostIntegrationSettingIDs.Embedded, true);

    // Authorization settings
    settings.set(OAuth2AuthorizationSettingIDs.ClientID, "");
    settings.set(OAuth2AuthorizationSettingIDs.RedirectURL, "");

    return settings;
}
