from sqlalchemy import Engine
from sqlalchemy.orm import Session

from common.py.data.storage import StoragePool
from common.py.utils.config import Configuration

from .database_authorization_token_storage import DatabaseAuthorizationTokenStorage
from .database_connector_storage import DatabaseConnectorStorage
from .database_project_job_storage import DatabaseProjectJobStorage
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
        from .engines import create_database_engine

        DatabaseStoragePool._engine = create_database_engine(config)
        DatabaseStoragePool._schema = DatabaseSchema(DatabaseStoragePool._engine)

        DatabaseStoragePool._schema.prepare()

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
        self._project_job_storage = DatabaseProjectJobStorage(
            self._session, DatabaseStoragePool._schema.project_jobs_table
        )
        self._authorization_token_storage = DatabaseAuthorizationTokenStorage(
            self._session, DatabaseStoragePool._schema.authorization_tokens_table
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

    @property
    def project_job_storage(self) -> DatabaseProjectJobStorage:
        return self._project_job_storage

    @property
    def authorization_token_storage(self) -> DatabaseAuthorizationTokenStorage:
        return self._authorization_token_storage
