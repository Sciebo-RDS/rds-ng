import abc

from .storage import Storage
from ..entities import Connector, ConnectorID


class ConnectorStorage(Storage[Connector, ConnectorID], abc.ABC):
    """
    Storage for connectors.
    """
