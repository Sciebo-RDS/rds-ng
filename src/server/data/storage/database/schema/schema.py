from sqlalchemy import MetaData, Engine, Table
from sqlalchemy.orm import registry

from .table_connectors import register_connectors_table


class DatabaseSchema:
    """
    The overall database schema.
    """

    def __init__(self, engine: Engine):
        self._engine = engine

        self._metadata = MetaData()
        self._registry = registry(metadata=self._metadata)

        # Register all tables
        self._connectors_table = register_connectors_table(
            self._metadata, self._registry
        )
        self._users_table = Table("dummy", self._metadata)
        self._projects_table = Table("dummy_2", self._metadata)

        # Create all registered tables
        self._metadata.create_all(self._engine)

    @property
    def connectors_table(self) -> Table:
        return self._connectors_table

    @property
    def users_table(self) -> Table:
        return self._users_table

    @property
    def projects_table(self) -> Table:
        return self._projects_table
