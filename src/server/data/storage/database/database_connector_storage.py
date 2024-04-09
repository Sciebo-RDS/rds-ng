import typing

from sqlalchemy import Engine, Table

from common.py.data.entities.connector import ConnectorID, Connector
from common.py.data.storage import ConnectorStorage

from .database_storage_accessor import DatabaseStorageAccessor


class DatabaseConnectorStorage(ConnectorStorage):
    """
    Database storage for connectors.
    """

    def __init__(self, engine: Engine, table: Table):
        super().__init__()

        self._engine = engine
        self._table = table

        self._accessor = DatabaseStorageAccessor[Connector, ConnectorID](
            Connector, self._engine, self._lock
        )

    def next_id(self) -> ConnectorID:
        raise NotImplementedError("Connectors do not support automatic IDs")

    def add(self, entity: Connector) -> None:
        self._accessor.add(entity)

    def remove(self, entity: Connector) -> None:
        self._accessor.remove(entity)

    def get(self, key: ConnectorID) -> Connector | None:
        return self._accessor.get(key)

    def list(self) -> typing.List[Connector]:
        return self._accessor.list()
