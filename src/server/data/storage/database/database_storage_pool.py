from sqlalchemy import create_engine

from common.py.data.storage import StoragePool
from common.py.utils.config import Configuration

from .database_connector_storage import DatabaseConnectorStorage
from .database_project_storage import DatabaseProjectStorage
from .database_user_storage import DatabaseUserStorage
from .schema import DatabaseSchema


class DatabaseStoragePool(StoragePool):
    """
    A generic database storage pool, based on SQLAlchemy.
    """

    def __init__(self, config: Configuration):
        super().__init__("Database", config)

        from common.py.settings import GeneralSettingIDs

        # TODO: Config/Driver
        from sqlalchemy import StaticPool

        self._engine = create_engine(
            "sqlite:///:memory:",
            echo=config.value(GeneralSettingIDs.DEBUG),
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        self._schema = DatabaseSchema(self._engine)

        self._connector_storage = DatabaseConnectorStorage(
            self._engine, self._schema.connectors_table
        )
        self._project_storage = DatabaseProjectStorage(self._engine)
        self._user_storage = DatabaseUserStorage(self._engine)

        # TODO: Remove later
        from ...._stub_.data import get_stub_data_connectors

        for con in get_stub_data_connectors():
            self._connector_storage.add(con)

    @property
    def connector_storage(self) -> DatabaseConnectorStorage:
        return self._connector_storage

    @property
    def user_storage(self) -> DatabaseUserStorage:
        return self._user_storage

    @property
    def project_storage(self) -> DatabaseProjectStorage:
        return self._project_storage
