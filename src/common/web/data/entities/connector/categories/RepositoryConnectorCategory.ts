import { ConnectorCategory, type ConnectorCategoryID } from "./ConnectorCategory";

export class RepositoryConnectorCategory extends ConnectorCategory {
    public static readonly CategoryID: ConnectorCategoryID = "repository";

    public constructor() {
        super("Repository", "Publish your project to make it available to the public.");
    }
}
