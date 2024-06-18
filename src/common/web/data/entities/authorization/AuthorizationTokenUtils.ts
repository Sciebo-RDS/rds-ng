import { ConnectorInstance } from "../connector/ConnectorInstance";
import { AuthorizationTokenType } from "./AuthorizationToken";

/**
 * Formats the authorization ID for a connector instance.
 *
 * @param instance - The connector instance.
 *
 * @returns - The authorization ID.
 */
export function getConnectorInstanceAuthorizationID(instance: ConnectorInstance): string {
    return `${AuthorizationTokenType.Connector}:${instance.instance_id}`;
}
