import { SettingID } from "@common/utils/config/SettingID";

/**
 * Identifiers for integration settings.
 *
 * @property Scheme - The integration scheme to use (value type: ``string``).
 */
export class IntegrationSettingIDS {
    public static readonly Scheme = new SettingID("integration", "scheme");
}

/**
 * Identifiers for host integration settings.
 *
 * @property APIURL - The URL where the host integration exposes its API (value type: ``string``).
 * @property Embedded - Whether the integration is embedded in an iframe (value type: ``boolean``).
 */
export class HostIntegrationSettingIDs {
    public static readonly APIURL = new SettingID("integration.host", "api_url");

    public static readonly Embedded = new SettingID("integration.host", "embedded");
}
