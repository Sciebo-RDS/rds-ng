import { WebComponent } from "../../../component/WebComponent";
import { AuthorizationStrategy } from "../../../integration/authorization/strategies/AuthorizationStrategy";
import { Service } from "../../../services/Service";
import { Connector, type ConnectorID } from "./Connector";
import { ConnectorInstance, type ConnectorInstanceID } from "./ConnectorInstance";
import { createAuthorizationStrategyFromConnector, findConnectorByID, findConnectorInstanceByID } from "./ConnectorUtils";

/**
 * A single connector instances group.
 */
export interface ConnectorInstancesGroup {
    connectorID: ConnectorID;
    connectorInstances: ConnectorInstance[];
}

/**
 * Function to return all connector instances grouped by their used connectors. By default, the groups are sorted by their IDs; if a list of
 * connectors is given, the display name is used instead.
 *
 * @param connectorInstances - The connector instances.
 * @param connectors - List of available connectors used to sort the groups by their display names.
 *
 * @return - The grouped connector instances.
 */
export function groupConnectorInstances(connectorInstances: ConnectorInstance[], connectors?: Connector[]): ConnectorInstancesGroup[] {
    const instancesGroups = [] as ConnectorInstancesGroup[];
    connectorInstances.forEach((instance) => {
        let group = instancesGroups.find((group) => group.connectorID == instance.connector_id);
        if (!group) {
            group = {
                connectorID: instance.connector_id,
                connectorInstances: [] as ConnectorInstance[],
            };
            instancesGroups.push(group);
        }
        group.connectorInstances.push(instance);
    });

    instancesGroups.sort((group1, group2) => {
        if (connectors) {
            const connector1 = findConnectorByID(connectors, group1.connectorID);
            const connector2 = findConnectorByID(connectors, group2.connectorID);

            if (connector1 && connector2) {
                return connector1.name.toLowerCase().localeCompare(connector2.name.toLowerCase());
            }
        }

        return group1.connectorID.toLowerCase().localeCompare(group2.connectorID.toLowerCase());
    });

    return instancesGroups;
}

/**
 * Searches for a connector using a connector instance ID.
 * @param connectors - The list of connectors.
 * @param connectorInstances - The list of connector instances.
 * @param instanceID - The connector instance ID.
 *
 * @returns - The found connector or **undefined** otherwise.
 */
export function findConnectorByInstanceID(
    connectors: Connector[],
    connectorInstances: ConnectorInstance[],
    instanceID: ConnectorInstanceID,
): Connector | undefined {
    const instance = findConnectorInstanceByID(connectorInstances, instanceID);
    return instance ? findConnectorByID(connectors, instance.connector_id) : undefined;
}

/**
 * Creates the authorization strategy configured in a connector instance.
 *
 * @param comp - The global component.
 * @param svc - The service to use for message sending.
 * @param instance - The connector instance.
 * @param connectors - List of all connectors.
 *
 * @returns - The authorization strategy or **undefined** if none is required.
 */
export function createAuthorizationStrategyFromConnectorInstance(
    comp: WebComponent,
    svc: Service,
    instance: ConnectorInstance,
    connectors: Connector[],
): AuthorizationStrategy | undefined {
    const connector = findConnectorByID(connectors, instance.connector_id);
    return createAuthorizationStrategyFromConnector(comp, svc, connector);
}
