from common.py.utils.items_catalog import ItemsCatalog
from connectors.base.metadata import ConnectorMetadataFactory


@ItemsCatalog.define()
class ConnectorMetadataFactoryCatalog(ItemsCatalog[ConnectorMetadataFactory]):
    """
    Global catalog of connector metadata factories.
    """
