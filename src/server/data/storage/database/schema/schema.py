from sqlalchemy import MetaData, Engine, Table
from sqlalchemy.orm import registry, Session

from .table_connectors import register_connectors_tables
from .table_users import register_users_tables
from .table_projects import register_projects_tables
from .table_project_jobs import register_project_jobs_tables


class DatabaseSchema:
    """
    The overall database schema.
    """

    def __init__(self, engine: Engine):
        self._engine = engine

        self._metadata = MetaData()
        self._registry = registry(metadata=self._metadata)

        # Register all tables
        self._connectors_tables = register_connectors_tables(
            self._metadata, self._registry
        )
        self._users_tables = register_users_tables(self._metadata, self._registry)
        self._projects_tables = register_projects_tables(self._metadata, self._registry)
        self._project_jobs_tables = register_project_jobs_tables(
            self._metadata, self._registry
        )

        # Create all registered tables
        self._metadata.create_all(self._engine)

    def prepare(self) -> None:
        with Session(self._engine) as session, session.begin():
            # Delete all connectors from the table, as they are always added anew on restart
            session.execute(self._connectors_tables.main.delete())

            # Project jobs are also not kept persistent across restarts
            session.execute(self._project_jobs_tables.main.delete())

    @property
    def connectors_table(self) -> Table:
        return self._connectors_tables.main

    @property
    def users_table(self) -> Table:
        return self._users_tables.main

    @property
    def projects_table(self) -> Table:
        return self._projects_tables.main

    @property
    def project_jobs_table(self) -> Table:
        return self._project_jobs_tables.main
