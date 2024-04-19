import typing
from dataclasses import dataclass

from .connector_category import ConnectorCategory, ConnectorCategoryID
from .connector_categories_catalog import ConnectorCategoriesCatalog


@dataclass(frozen=True, kw_only=True)
class ArchiveConnectorCategory(ConnectorCategory):
    category_id: typing.ClassVar[ConnectorCategoryID] = "archive"

    def __init__(self):
        super().__init__(
            name="Archive",
            description="Store your project data in a long-term external storage archive.",
        )


ConnectorCategoriesCatalog.register_item(
    ArchiveConnectorCategory.category_id, ArchiveConnectorCategory()
)
