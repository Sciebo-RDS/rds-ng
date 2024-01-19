import { Connector, type ConnectorID } from "./Connector";
import { ConnectorInstance } from "./ConnectorInstance";

/**
 * A single connector instances group.
 */
export interface ConnectorInstancesGroup {
    connectorID: ConnectorID;
    connectorInstances: ConnectorInstance[];
}

/**
 * Function to return all connector instances grouped by their used connectors.
 *
 * @param connectorInstances - The connector instances.
 *
 * @return - The grouped connector instances.
 */
export function groupConnectorInstances(connectorInstances: ConnectorInstance[]): ConnectorInstancesGroup[] {
    const instancesGroups = [] as ConnectorInstancesGroup[];
    connectorInstances.forEach((instance) => {
        let group = instancesGroups.find((group) => group.connectorID == instance.connector_id);
        if (!group) {
            group = {
                connectorID: instance.connector_id,
                connectorInstances: [] as ConnectorInstance[]
            };
            instancesGroups.push(group);
        }
        group.connectorInstances.push(instance);
    });
    return instancesGroups;
}

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
