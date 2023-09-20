import abc

from .project_storage import ProjectStorage


class StoragePool(abc.ABC):
    """
    A collection of all data storages.
    """

    @property
    @abc.abstractmethod
    def project_storage(self) -> ProjectStorage:
        """
        The project storage.
        """
        raise NotImplementedError
