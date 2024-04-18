from common.py.data.storage import StoragePool

from .memory_connector_storage import MemoryConnectorStorage
from .memory_project_storage import MemoryProjectStorage
from .memory_user_storage import MemoryUserStorage


class MemoryStoragePool(StoragePool):
    """
    A simple, non-persistent in-memory storage pool.
    """

    def __init__(self):
        super().__init__("Memory")

        self._connector_storage = MemoryConnectorStorage()
        self._project_storage = MemoryProjectStorage()
        self._user_storage = MemoryUserStorage()

    @property
    def connector_storage(self) -> MemoryConnectorStorage:
        return self._connector_storage

    @property
    def user_storage(self) -> MemoryUserStorage:
        return self._user_storage

    @property
    def project_storage(self) -> MemoryProjectStorage:
        return self._project_storage
