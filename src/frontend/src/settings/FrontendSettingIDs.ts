import { SettingID } from "@common/utils/config/SettingID";

/**
 * Identifiers for frontend settings.
 *
 * @property RegularCommandTimeout - The timeout in seconds for commands which are usually executed quickly (value type: ``number``).
 */
export class FrontendSettingIDs {
    public static readonly RegularCommandTimeout = new SettingID("frontend", "regular_command_timeout");
}
