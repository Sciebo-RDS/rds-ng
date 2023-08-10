import { SettingID } from "../utils/config/SettingID";

/**
 * Identifiers for client-specific networking settings.
 *
 * @property ServerAddress - The address of the server the client should automatically connect to (value type: ``string``).
 * @property ConnectionTimeout - The maximum time (in seconds) for connection attempts (value type: ``float``).
 */
export class NetworkSettingIDs {
    public static readonly ServerAddress = new SettingID("network.client", "server_address");
    public static readonly ConnectionTimeout = new SettingID("network.client", "connection_timeout");
}
