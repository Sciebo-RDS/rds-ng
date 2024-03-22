import abc

from .connector_storage import ConnectorStorage
from .project_storage import ProjectStorage


class StoragePool(abc.ABC):
    # pylint: disable=too-few-public-methods
    """
    A collection of all data storages.
    """

    def __init__(self, name: str):
        """
        Args:
            name: The name of the storage pool.
        """
        self._name = name

    @property
    def name(self) -> str:
        """
        The name of this backend.
        """
        return self._name

    @property
    @abc.abstractmethod
    def connector_storage(self) -> ConnectorStorage:
        """
        The connector storage.
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def project_storage(self) -> ProjectStorage:
        """
        The project storage.
        """
        raise NotImplementedError()
