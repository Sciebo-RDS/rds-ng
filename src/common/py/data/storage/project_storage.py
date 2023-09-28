import abc

from .storage import Storage
from ..entities import Project, ProjectID


class ProjectStorage(Storage[Project, ProjectID], abc.ABC):
    """
    Storage for projects.
    """

    def __init__(self):
        import threading

        self._lock = threading.RLock()
