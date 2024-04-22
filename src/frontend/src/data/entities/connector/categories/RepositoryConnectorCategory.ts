import { type ConnectorCategoryID } from "@common/data/entities/connector/Connector";

import { ConnectorCategory } from "./ConnectorCategory";

export class RepositoryConnectorCategory extends ConnectorCategory {
    public static readonly CategoryID: ConnectorCategoryID = "repository";

    public constructor() {
        super(
            "Repository",
            "Publish your project to make it available to the public.",
            "Publish",
            "r-connector-category-repository-tag",
            "r-connector-category-repository-button",
        );
    }
}
