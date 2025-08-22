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
 * @property URL - The full URL of the host (value type: ``string``).
 * @property EntrypointEndpoint - The relative entrypoint path of the host integration app (value type: ``string``).
 * @property APIEndpoint - The relative path of the host integration API (value type: ``string``).
 */
export class HostIntegrationSettingIDs {
    public static readonly URL = new SettingID("integration.host", "url");
    public static readonly EntrypointEndpoint = new SettingID("integration.host.endpoints", "entrypoint");
    public static readonly APIEndpoint = new SettingID("integration.host.endpoints", "api");
}
