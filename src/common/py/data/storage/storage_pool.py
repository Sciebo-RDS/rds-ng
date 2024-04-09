import abc

from .connector_storage import ConnectorStorage
from .project_storage import ProjectStorage
from .user_storage import UserStorage
from ...utils.config import Configuration


class StoragePool(abc.ABC):
    """
    A collection of all data storages.
    """

    def __init__(self, name: str, config: Configuration):
        """
        Args:
            name: The name of the storage pool.
            config: The global configuration.
        """
        self._name = name
        self._config = config

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
    def user_storage(self) -> UserStorage:
        """
        The user storage.
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def project_storage(self) -> ProjectStorage:
        """
        The project storage.
        """
        raise NotImplementedError()
