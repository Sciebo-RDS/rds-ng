from common.py.data.storage import StoragePool, ProjectStorage, ConnectorStorage


class MemoryStoragePool(StoragePool):
    # pylint: disable=too-few-public-methods
    """
    A simple, non-persistent in-memory storage pool.

    Args:
        connector_storage_id: The ID of the connector storage.
        project_storage_id: The ID of the project storage.
    """

    def __init__(
        self,
        *,
        connector_storage_id: str = "_global_",
        project_storage_id: str = "_global_"
    ):
        self._connector_storage_id = connector_storage_id
        self._project_storage_id = project_storage_id

    @property
    def connector_storage(self) -> ConnectorStorage:
        from .memory_connector_storage import MemoryConnectorStorage

        return MemoryConnectorStorage(self._connector_storage_id)

    @property
    def project_storage(self) -> ProjectStorage:
        from .memory_project_storage import MemoryProjectStorage

        return MemoryProjectStorage(self._project_storage_id)
