from common.py.data.metadata import MetadataCreator
from common.py.utils.items_catalog import ItemsCatalog


@ItemsCatalog.define()
class MetadataCreatorCatalog(ItemsCatalog[MetadataCreator]):
    """
    Global catalog of connector metadata factories.
    """
