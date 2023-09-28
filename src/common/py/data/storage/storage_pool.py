import abc

from .project_storage import ProjectStorage


class StoragePool(abc.ABC):
    # pylint: disable=too-few-public-methods
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
