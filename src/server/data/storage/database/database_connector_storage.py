import typing

from sqlalchemy import Engine, select, Table
from sqlalchemy.orm import Session

from common.py.data.entities.connector import ConnectorID, Connector
from common.py.data.storage import ConnectorStorage


class DatabaseConnectorStorage(ConnectorStorage):
    """
    Database storage for connectors.
    """

    def __init__(self, engine: Engine, table: Table):
        super().__init__()

        self._engine = engine
        self._table = table

    def next_id(self) -> ConnectorID:
        raise NotImplementedError("Connectors do not support automatic IDs")

    def add(self, entity: Connector) -> None:
        with self._lock:
            with Session(self._engine) as session:
                with session.begin():
                    session.add(entity)

    def remove(self, entity: Connector) -> None:
        with self._lock:
            with Session(self._engine) as session:
                with session.begin():
                    session.delete(entity)

    def get(self, key: ConnectorID) -> Connector | None:
        with self._lock:
            with Session(self._engine) as session:
                return typing.cast(
                    Connector | None,
                    session.execute(
                        select(Connector).where(self._table.c.connector_id == key)
                    ).scalar(),
                )

    def list(self) -> typing.List[Connector]:
        with self._lock:
            with Session(self._engine) as session:
                return typing.cast(
                    typing.List[Connector],
                    session.execute(select(Connector)).scalars().all(),
                )
