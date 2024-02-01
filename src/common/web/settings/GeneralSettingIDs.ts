import { SettingID } from "../utils/config/SettingID";

/**
 * Identifiers for general settings.
 *
 * @property Debug - Whether debug mode should be enabled (value type: ``bool``).
 * @property NotificationTimeout - The timeout for overlay notifications in seconds (value type: ``number``).
 */
export class GeneralSettingIDs {
    public static readonly Debug = new SettingID("general", "debug");

    public static readonly NotificationTimeout = new SettingID("general", "notification_timeout");
}
