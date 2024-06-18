import { AuthorizationStrategiesCatalog } from "../../../integration/authorization/strategies/AuthorizationStrategiesCatalog";
import { Connector, type ConnectorID } from "./Connector";
import { ConnectorInstance, type ConnectorInstanceID } from "./ConnectorInstance";

/**
 * Searches for a connector by its ID within a list of connectors.
 *
 * @param connectors - The list of connectors.
 * @param connectorID - The connector to search for.
 *
 * @returns - The found connector or **undefined** otherwise.
 */
export function findConnectorByID(connectors: Connector[], connectorID: ConnectorID): Connector | undefined {
    return connectors.find((con) => con.connector_id == connectorID);
}

/**
 * Searches for a connector instance by its ID within a list of connector instances.
 *
 * @param connectorInstances - The list of connector instances.
 * @param instanceID - The connector instance to search for.
 *
 * @returns - The found connector instance or **undefined** otherwise.
 */
export function findConnectorInstanceByID(connectorInstances: ConnectorInstance[], instanceID: ConnectorInstanceID): ConnectorInstance | undefined {
    return connectorInstances.find((inst) => inst.instance_id == instanceID);
}

/**
 * Checks whether a connector requires authorization (and whether that authorization strategy is available).
 *
 * @param connector - The connector.
 */
export function connectorRequiresAuthorization(connector: Connector): boolean {
    const strategy = connector.authorization.strategy;
    return strategy != "" && AuthorizationStrategiesCatalog.findItem(strategy) != undefined;
}
