from common.py.utils import ItemsCatalog

from .backend import Backend


@ItemsCatalog.define()
class BackendsCatalog(ItemsCatalog[type[Backend]]):
    """
    Global catalog of all registered backend types.

    This is a globally accessible list of all backend types, associated with their respective names.
    """
