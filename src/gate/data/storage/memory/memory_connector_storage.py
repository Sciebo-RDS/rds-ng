import threading
import typing

from common.py.data.entities.connector import ConnectorID, Connector
from common.py.data.storage import ConnectorStorage


class MemoryConnectorStorage(ConnectorStorage):
    """
    In-memory storage for connectors.

    Args:
        storage_id: If set, the session storage is used instead of the global one.
    """

    default_connectors: typing.List[Connector] = []

    _global_connectors: typing.Dict[str, typing.Dict[ConnectorID, Connector]] = {}

    _lock = threading.RLock()

    def __init__(self, storage_id: str):
        super().__init__()

        self._storage_id = storage_id

        has_storage = self._storage_id in MemoryConnectorStorage._global_connectors
        if not has_storage:
            MemoryConnectorStorage._global_connectors[storage_id] = {}

        self._connectors = MemoryConnectorStorage._global_connectors[storage_id]

        if not has_storage:
            from common.py.data.entities import clone_entity

            for connector in MemoryConnectorStorage.default_connectors:
                self.add(clone_entity(connector))

    def next_id(self) -> ConnectorID:
        raise NotImplementedError("Connectors do not support automatic IDs")

    def add(self, entity: Connector) -> None:
        with MemoryConnectorStorage._lock:
            self._connectors[entity.connector_id] = entity

    def remove(self, entity: Connector) -> None:
        with MemoryConnectorStorage._lock:
            try:
                del self._connectors[entity.connector_id]
            except Exception as exc:  # pylint: disable=broad-exception-caught
                from common.py.data.storage import StorageException

                raise StorageException(
                    f"A connector with ID {entity.connector_id} was not found"
                ) from exc

    def get(self, key: ConnectorID) -> Connector | None:
        with MemoryConnectorStorage._lock:
            if key in self._connectors:
                return self._connectors[key]
            return None

    def list(self) -> typing.List[Connector]:
        with MemoryConnectorStorage._lock:
            return list(self._connectors.values())
