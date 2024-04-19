import { type ConnectorCategoryID } from "@common/data/entities/connector/Connector";

import { ConnectorCategory } from "./ConnectorCategory";

export class ArchiveConnectorCategory extends ConnectorCategory {
    public static readonly CategoryID: ConnectorCategoryID = "archive";

    public constructor() {
        super("Archive", "Store your project data in a long-term external storage archive.");
    }
}
