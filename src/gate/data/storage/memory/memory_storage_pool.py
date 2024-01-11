from common.py.data.storage import StoragePool, ProjectStorage, ConnectorStorage


class MemoryStoragePool(StoragePool):
    # pylint: disable=too-few-public-methods
    """
    A simple, non-persistent in-memory storage pool.
    """

    @property
    def connector_storage(self) -> ConnectorStorage:
        from .memory_connector_storage import MemoryConnectorStorage

        return MemoryConnectorStorage()

    @property
    def project_storage(self) -> ProjectStorage:
        from .memory_project_storage import MemoryProjectStorage

        return MemoryProjectStorage()
