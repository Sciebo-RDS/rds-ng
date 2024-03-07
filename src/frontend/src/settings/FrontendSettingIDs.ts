import { SettingID } from "@common/utils/config/SettingID";

/**
 * Identifiers for frontend settings.
 *
 * @property RegularCommandTimeout - The timeout in seconds for commands which are usually executed quickly (value type: ``number``).
 * @property AuthenticationScheme - The authentication scheme to use (value type: ``string``).
 */
export class FrontendSettingIDs {
    public static readonly RegularCommandTimeout = new SettingID("frontend", "regular_command_timeout");

    public static readonly PublicKeyURL = new SettingID("frontend", "public_key_url"); // TODO: Temporary

    public static readonly AuthenticationScheme = new SettingID("frontend", "authentication_scheme");
}
