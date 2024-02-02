import typing

from common.py.data.entities.connector import ConnectorID, Connector
from common.py.data.storage import ConnectorStorage
from common.py.utils import UnitID


class MemoryConnectorStorage(ConnectorStorage):
    """
    In-memory storage for connectors.

    Args:
        session_id: If set, the session storage is used instead of the global one.
    """

    _global_connectors: typing.Dict[ConnectorID, Connector] = {}

    def __init__(self, session_id: UnitID | None = None):
        super().__init__()

        self._connectors = MemoryConnectorStorage._global_connectors
        if session_id:
            from ..session import SessionStorage

            self._connectors = SessionStorage().get_data(
                session_id,
                "connectors",
                typing.cast(typing.Dict[ConnectorID, Connector], {}),
            )

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
            if key in self._connectors:
                return self._connectors[key]
            return None

    def list(self) -> typing.List[Connector]:
        with self._lock:
            return list(self._connectors.values())
