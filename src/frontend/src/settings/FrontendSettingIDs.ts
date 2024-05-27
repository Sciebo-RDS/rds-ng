import { SettingID } from "@common/utils/config/SettingID";

/**
 * Identifiers for frontend settings.
 *
 * @property RegularCommandTimeout - The timeout in seconds for commands which are usually executed quickly (value type: ``number``).
 * @property HostAPIURL - The URL where the host integration exposes its API.
 * @property IntegrationScheme - The integration scheme to use (value type: ``string``).
 */
export class FrontendSettingIDs {
    public static readonly RegularCommandTimeout = new SettingID("frontend", "regular_command_timeout");

    public static readonly HostAPIURL = new SettingID("frontend", "host_api_url");

    public static readonly IntegrationScheme = new SettingID("frontend", "integration_scheme");
}
