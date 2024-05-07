import { ArchiveConnectorCategory } from "./ArchiveConnectorCategory";
import { ConnectorCategoriesCatalog } from "./ConnectorCategoriesCatalog";
import { RepositoryConnectorCategory } from "./RepositoryConnectorCategory";

export function registerConnectorCategories(): void {
    // New categories must be registered here
    ConnectorCategoriesCatalog.registerItem(RepositoryConnectorCategory.CategoryID, new RepositoryConnectorCategory());
    ConnectorCategoriesCatalog.registerItem(ArchiveConnectorCategory.CategoryID, new ArchiveConnectorCategory());
}
