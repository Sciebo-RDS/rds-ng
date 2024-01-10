import abc

from .connector_storage import ConnectorStorage
from .project_storage import ProjectStorage


class StoragePool(abc.ABC):
    # pylint: disable=too-few-public-methods
    """
    A collection of all data storages.
    """

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
