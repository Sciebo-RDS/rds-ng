from .database_connector_storage import DatabaseConnectorStorage
from .database_project_storage import DatabaseProjectStorage
from .database_user_storage import DatabaseUserStorage

from .database_storage_pool import DatabaseStoragePool

from .. import StoragePoolsCatalog

StoragePoolsCatalog.register_item("database", DatabaseStoragePool)
