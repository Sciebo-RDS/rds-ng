import typing
from dataclasses import dataclass

from .connector_category import ConnectorCategory, ConnectorCategoryID
from .connector_categories_catalog import ConnectorCategoriesCatalog


@dataclass(frozen=True, kw_only=True)
class RepositoryConnectorCategory(ConnectorCategory):
    category_id: typing.ClassVar[ConnectorCategoryID] = "repository"

    def __init__(self):
        super().__init__(
            name="Repository",
            description="Publish your project to make it available to the public.",
        )


ConnectorCategoriesCatalog.register_item(
    RepositoryConnectorCategory.category_id, RepositoryConnectorCategory()
)
