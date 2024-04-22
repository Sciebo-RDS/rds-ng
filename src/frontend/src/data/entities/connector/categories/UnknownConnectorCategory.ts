import { type ConnectorCategoryID } from "@common/data/entities/connector/Connector";

import { ConnectorCategory } from "./ConnectorCategory";

export class UnknownConnectorCategory extends ConnectorCategory {
    public static readonly CategoryID: ConnectorCategoryID = "unknown";

    public constructor() {
        super("Unknown", "A connector with no specific or an unknown category.", "r-connector-category-unknown-tag");
    }
}
