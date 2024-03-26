from common.py.data.storage import StoragePool

from .memory_connector_storage import MemoryConnectorStorage
from .memory_project_storage import MemoryProjectStorage
from .memory_user_storage import MemoryUserStorage


class MemoryStoragePool(StoragePool):
    # pylint: disable=too-few-public-methods
    """
    A simple, non-persistent in-memory storage pool.
    """

    _connectors_added: bool = False

    def __init__(self):
        super().__init__("Memory")

        # TODO: Remove later
        if not MemoryStoragePool._connectors_added:
            from ...._stub_.data import get_stub_data_connectors

            for con in get_stub_data_connectors():
                self.connector_storage.add(con)

            MemoryStoragePool._connectors_added = True

    @property
    def connector_storage(self) -> MemoryConnectorStorage:
        return MemoryConnectorStorage()

    @property
    def user_storage(self) -> MemoryUserStorage:
        return MemoryUserStorage()

    @property
    def project_storage(self) -> MemoryProjectStorage:
        return MemoryProjectStorage()
