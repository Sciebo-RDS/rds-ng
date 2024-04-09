import threading
import typing

from sqlalchemy import Engine

from common.py.data.entities.connector import ConnectorID, Connector
from common.py.data.storage import ConnectorStorage


class DatabaseConnectorStorage(ConnectorStorage):
    """
    Database storage for connectors.
    """

    def __init__(self, engine: Engine):
        super().__init__()

        self._engine = engine

        self._lock = threading.RLock()

    def next_id(self) -> ConnectorID:
        raise NotImplementedError("Connectors do not support automatic IDs")

    def add(self, entity: Connector) -> None:
        pass

    def remove(self, entity: Connector) -> None:
        pass

    def get(self, key: ConnectorID) -> Connector | None:
        pass

    def list(self) -> typing.List[Connector]:
        pass
