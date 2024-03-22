from .memory_connector_storage import MemoryConnectorStorage
from .memory_project_storage import MemoryProjectStorage

from .memory_storage_pool import MemoryStoragePool

from .. import StoragePoolsCatalog

StoragePoolsCatalog.register_item("memory", MemoryStoragePool)
