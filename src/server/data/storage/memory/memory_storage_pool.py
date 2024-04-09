from common.py.data.storage import StoragePool
from common.py.utils.config import Configuration

from .memory_connector_storage import MemoryConnectorStorage
from .memory_project_storage import MemoryProjectStorage
from .memory_user_storage import MemoryUserStorage


class MemoryStoragePool(StoragePool):
    """
    A simple, non-persistent in-memory storage pool.
    """

    def __init__(self, config: Configuration):
        super().__init__("Memory", config)

        self._connector_storage = MemoryConnectorStorage()
        self._project_storage = MemoryProjectStorage()
        self._user_storage = MemoryUserStorage()

        # TODO: Remove later
        from ...._stub_.data import get_stub_data_connectors

        for con in get_stub_data_connectors():
            self._connector_storage.add(con)

    @property
    def connector_storage(self) -> MemoryConnectorStorage:
        return self._connector_storage

    @property
    def user_storage(self) -> MemoryUserStorage:
        return self._user_storage

    @property
    def project_storage(self) -> MemoryProjectStorage:
        return self._project_storage
