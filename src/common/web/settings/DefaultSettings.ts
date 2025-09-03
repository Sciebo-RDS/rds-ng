import { ThemeSettings } from "../ui/theme/ThemeSettings";
import { SettingID } from "../utils/config/SettingID";
import { GeneralSettingIDs } from "./GeneralSettingIDs";
import { NetworkClientSettingIDs, NetworkSettingIDs } from "./NetworkSettingIDs";
import { ThemeSettingIDs } from "./ThemeSettingIDs";

/**
 * Gets default values for all settings.
 *
 * @returns - An object mapping the setting identifiers to their default values.
 */
export function getDefaultSettings(): Map<SettingID, any> {
    let defaults = new Map<SettingID, any>();

    // General settings
    defaults.set(GeneralSettingIDs.Debug, false);
    defaults.set(GeneralSettingIDs.SupportEmail, "sciebo.rds@uni-muenster.de");
    defaults.set(GeneralSettingIDs.VerboseNotifications, false);
    defaults.set(GeneralSettingIDs.NotificationTimeout, 3.0);

    // Network settings
    defaults.set(NetworkSettingIDs.RegularCommandTimeout, 10.0);
    defaults.set(NetworkClientSettingIDs.ServerAddress, "");
    defaults.set(NetworkClientSettingIDs.ConnectionTimeout, 10.0);

    // Theme settings
    defaults.set(ThemeSettingIDs.PrimaryColor, ThemeSettings.primaryColor);
    defaults.set(ThemeSettingIDs.LightSurfaceColor, ThemeSettings.light.surfaceColor);
    defaults.set(ThemeSettingIDs.LightHighlightColor, ThemeSettings.light.highlightColor);
    defaults.set(ThemeSettingIDs.DarkSurfaceColor, ThemeSettings.dark.surfaceColor);
    defaults.set(ThemeSettingIDs.DarkHighlightColor, ThemeSettings.dark.highlightColor);

    return defaults;
}
