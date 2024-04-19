from .connector_category import ConnectorCategory
from common.py.utils import ItemsCatalog


@ItemsCatalog.define()
class ConnectorCategoriesCatalog(ItemsCatalog[ConnectorCategory]):
    """
    Global catalog of all connector categories.

    Categories are stored as fixed dataclasses describing each category.
    """
