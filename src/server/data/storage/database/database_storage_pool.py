from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from common.py.data.storage import StoragePool
from common.py.utils.config import Configuration

from .database_connector_storage import DatabaseConnectorStorage
from .database_project_storage import DatabaseProjectStorage
from .database_user_storage import DatabaseUserStorage
from .schema import DatabaseSchema


class DatabaseStoragePool(StoragePool):
    """
    Multi-backend database storage pool, based on SQLAlchemy.
    """

    _engine: Engine
    _schema: DatabaseSchema

    @staticmethod
    def prepare(config: Configuration) -> None:
        from ....settings.storage_setting_ids import DatabaseStorageSettingIDs

        # TODO: Config/Driver
        from sqlalchemy import StaticPool

        DatabaseStoragePool._engine = create_engine(
            "sqlite:///:memory:",
            echo=config.value(DatabaseStorageSettingIDs.DUMP_SQL),
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        DatabaseStoragePool._schema = DatabaseSchema(DatabaseStoragePool._engine)

        # TODO: Remove later
        from ...._stub_.data import get_stub_data_connectors

        with Session(DatabaseStoragePool._engine) as session, session.begin():
            connectors = DatabaseConnectorStorage(
                session,
                DatabaseStoragePool._schema.connectors_table,
            )

            for con in get_stub_data_connectors():
                connectors.add(con)

    def __init__(self):
        super().__init__("Database")

        self._session = Session(DatabaseStoragePool._engine)

        self._connector_storage = DatabaseConnectorStorage(
            self._session, DatabaseStoragePool._schema.connectors_table
        )
        self._user_storage = DatabaseUserStorage(
            self._session, DatabaseStoragePool._schema.users_table
        )
        self._project_storage = DatabaseProjectStorage(
            self._session, DatabaseStoragePool._schema.projects_table
        )

    def close(self, save_changes: bool = True) -> None:
        self._session.commit() if save_changes else self._session.rollback()
        self._session.close()

    @property
    def connector_storage(self) -> DatabaseConnectorStorage:
        return self._connector_storage

    @property
    def user_storage(self) -> DatabaseUserStorage:
        return self._user_storage

    @property
    def project_storage(self) -> DatabaseProjectStorage:
        return self._project_storage
