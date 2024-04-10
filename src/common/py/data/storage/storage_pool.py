import abc

from .connector_storage import ConnectorStorage
from .project_storage import ProjectStorage
from .user_storage import UserStorage
from ...utils.config import Configuration


class StoragePool(abc.ABC):
    """
    A collection of all data storages.
    """

    @staticmethod
    def prepare(config: Configuration) -> None:
        """
        Performs initial preparation of the storage pool.

        Args:
            config: The global configuration.
        """

    def __init__(self, name: str):
        """
        Args:
            name: The name of the storage pool.
        """
        self._name = name

    def begin(self) -> None:
        """
        Called initially when a new pool instance is being used.
        """

    def close(self, save_changes: bool = True) -> None:
        """
        Closes a single pool instance.
        """

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
