import { SettingID } from "../utils/config/SettingID";

/**
 * Identifiers for general settings.
 *
 * @property Debug - Whether debug mode should be enabled (value type: ``bool``).
 */
export class GeneralSettingIDs {
    public static readonly Debug = new SettingID("", "debug");
}
