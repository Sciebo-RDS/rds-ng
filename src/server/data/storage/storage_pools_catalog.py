from common.py.data.storage import StoragePool
from common.py.utils import ItemsCatalog


@ItemsCatalog.define()
class StoragePoolsCatalog(ItemsCatalog[type[StoragePool]]):
    """
    Global catalog of all registered storage pool types.

    This is a globally accessible list of all storage pool types, associated with their respective names.
    """
