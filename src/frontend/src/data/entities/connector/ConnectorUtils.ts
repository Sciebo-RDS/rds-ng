import { Connector } from "@common/data/entities/connector/Connector";

import { ConnectorCategoriesCatalog } from "@/data/entities/connector/categories/ConnectorCategoriesCatalog";
import { ConnectorCategory } from "@/data/entities/connector/categories/ConnectorCategory";

/**
 * Retrieves the category of a connector or undefined otherwise.
 */
export function getConnectorCategory(connector: Connector): ConnectorCategory | undefined {
    return ConnectorCategoriesCatalog.findItem(connector.category);
}
