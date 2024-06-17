import { Connector } from "../../data/entities/connector/Connector";
import { ConnectorInstance } from "../../data/entities/connector/ConnectorInstance";

/**
 * Helper function to request authorization for a connector instance.
 *
 * @param strategy - The strategy to use.
 * @param connector - The connector.
 * @param instance - The connector instance.
 */
export function requestConnectorInstanceAuthorization(strategy: string, connector: Connector, instance: ConnectorInstance): void {
    console.log("AYYYY REQUEST");
}

/**
 * Helper function to revoke authorization for a connector instance.
 *
 * @param strategy - The strategy to use.
 * @param connector - The connector.
 * @param instance - The connector instance.
 */
export function revokeConnectorInstanceAuthorization(strategy: string, connector: Connector, instance: ConnectorInstance): void {
    console.log("AYYYY REVOKE");
}
