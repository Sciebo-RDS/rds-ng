from common.py.data.storage import StoragePool

from .memory_connector_storage import MemoryConnectorStorage
from .memory_project_storage import MemoryProjectStorage


class MemoryStoragePool(StoragePool):
    # pylint: disable=too-few-public-methods
    """
    A simple, non-persistent in-memory storage pool.
    """

    def __init__(self):
        super().__init__("Memory")

    @property
    def connector_storage(self) -> MemoryConnectorStorage:
        return MemoryConnectorStorage()

    @property
    def project_storage(self) -> MemoryProjectStorage:
        return MemoryProjectStorage()
