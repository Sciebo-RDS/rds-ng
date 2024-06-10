from common.py.data.storage import StoragePool, AuthorizationTokenStorage

from .memory_authorization_token_storage import MemoryAuthorizationTokenStorage
from .memory_connector_storage import MemoryConnectorStorage
from .memory_project_job_storage import MemoryProjectJobStorage
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
        self._project_job_storage = MemoryProjectJobStorage()
        self._user_storage = MemoryUserStorage()
        self._authorization_token_storage = MemoryAuthorizationTokenStorage()

    @property
    def connector_storage(self) -> MemoryConnectorStorage:
        return self._connector_storage

    @property
    def user_storage(self) -> MemoryUserStorage:
        return self._user_storage

    @property
    def project_storage(self) -> MemoryProjectStorage:
        return self._project_storage

    @property
    def project_job_storage(self) -> MemoryProjectJobStorage:
        return self._project_job_storage

    @property
    def authorization_token_storage(self) -> AuthorizationTokenStorage:
        return self._authorization_token_storage
