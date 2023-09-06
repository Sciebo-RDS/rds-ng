import typing

from common.py.component import BackendComponent
from common.py.services import Service
from common.py.utils import ItemsCatalog

BackendCreator = typing.Callable[[BackendComponent], Service]


@ItemsCatalog.define()
class BackendsCatalog(ItemsCatalog[BackendCreator]):
    """
    Global catalog of all registered backend types.

    This is a globally accessible list of all backend types, associated with their respective names.
    """
