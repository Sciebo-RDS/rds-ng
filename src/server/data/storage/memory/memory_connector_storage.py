import typing

from common.py.data.entities.connector import ConnectorID, Connector
from common.py.data.storage import ConnectorStorage


class MemoryConnectorStorage(ConnectorStorage):
    """
    In-memory storage for connectors.
    """

    def __init__(self):
        super().__init__()

        self._connectors: typing.Dict[ConnectorID, Connector] = {}

    def next_id(self) -> ConnectorID:
        raise NotImplementedError("Connectors do not support automatic IDs")

    def add(self, entity: Connector) -> None:
        with self._lock:
            self._connectors[entity.connector_id] = entity

    def remove(self, entity: Connector) -> None:
        with self._lock:
            try:
                del self._connectors[entity.connector_id]
            except Exception as exc:  # pylint: disable=broad-exception-caught
                from common.py.data.storage import StorageException

                raise StorageException(
                    f"A connector with ID {entity.connector_id} was not found"
                ) from exc

    def get(self, key: ConnectorID) -> Connector | None:
        with self._lock:
            return self._connectors[key] if key in self._connectors else None

    def list(self) -> typing.List[Connector]:
        with self._lock:
            return list(self._connectors.values())
