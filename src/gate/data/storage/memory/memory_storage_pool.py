import typing

from common.py.data.entities.connector import Connector
from common.py.data.entities.project import Project
from common.py.data.storage import StoragePool
from .memory_connector_storage import MemoryConnectorStorage
from .memory_project_storage import MemoryProjectStorage


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
        default_connectors: typing.List[Connector] | None = None,
        project_storage_id: str = "_global_",
        default_projects: typing.List[Project] | None = None
    ):
        self._connector_storage_id = connector_storage_id
        self._default_connectors = default_connectors
        self._project_storage_id = project_storage_id
        self._default_projects = default_projects

    @property
    def connector_storage(self) -> MemoryConnectorStorage:
        return MemoryConnectorStorage(
            self._connector_storage_id, self._default_connectors
        )

    @property
    def project_storage(self) -> MemoryProjectStorage:
        return MemoryProjectStorage(self._project_storage_id, self._default_projects)
