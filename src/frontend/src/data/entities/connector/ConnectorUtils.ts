import { Connector } from "@common/data/entities/connector/Connector";

import { ConnectorCategoriesCatalog } from "@/data/entities/connector/categories/ConnectorCategoriesCatalog";
import { ConnectorCategory } from "@/data/entities/connector/categories/ConnectorCategory";
import { ConnectorInstance, type ConnectorInstanceID } from "@common/data/entities/connector/ConnectorInstance";
import { findConnectorByInstanceID } from "@common/data/entities/connector/ConnectorInstanceUtils";
import { ColorTable } from "@common/ui/components/propertyeditor/utils/ColorTable";

/**
 * Retrieves the category of a connector or undefined otherwise.
 */
export function findConnectorCategory(connector: Connector): ConnectorCategory | undefined {
    return ConnectorCategoriesCatalog.findItem(connector.category);
}

/**
 * Retrieves the category of a connector instance.
 *
 * @param connectors - The connectors.
 * @param connectorInstances - The connector instances.
 * @param instanceID - The instance ID.
 *
 * @returns - The connector category, if any.
 */
export function findConnectorCategoryByInstanceID(
    connectors: Connector[],
    connectorInstances: ConnectorInstance[],
    instanceID: ConnectorInstanceID
): ConnectorCategory | undefined {
    const connector = findConnectorByInstanceID(connectors, connectorInstances, instanceID);
    return connector ? findConnectorCategory(connector) : undefined;
}

/**
 * Assigns tag colors to all connectors.
 *
 * @param connectors - The list of connectors.
 */
export function assignConnectorProfileColors(connectors: Connector[]): void {
    for (const connector of connectors.sort((con1, con2) => con1.name.localeCompare(con2.name))) {
        try {
            const profileID = connector.metadata_profile.metadata.id[0];
            ColorTable.color(profileID);
        } catch (e) {
            // Just ignore any exceptions
        }
    }
}
