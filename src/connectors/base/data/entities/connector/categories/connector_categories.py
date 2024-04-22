from .connector_categories_catalog import ConnectorCategoriesCatalog


def register_connector_categories() -> None:
    from .archive_connector_category import ArchiveConnectorCategory
    from .repository_connector_category import RepositoryConnectorCategory

    # New categories must be registered here
    ConnectorCategoriesCatalog.register_item(
        ArchiveConnectorCategory.category_id, ArchiveConnectorCategory()
    )
    ConnectorCategoriesCatalog.register_item(
        RepositoryConnectorCategory.category_id, RepositoryConnectorCategory()
    )
