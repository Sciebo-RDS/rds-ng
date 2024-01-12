import abc

from .storage import Storage
from ..entities.project import Project, ProjectID


class ProjectStorage(Storage[Project, ProjectID], abc.ABC):
    """
    Storage for projects.
    """
