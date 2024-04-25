import abc

from .storage import Storage
from ..entities.project import ProjectJob, ProjectJobID


class ProjectJobStorage(Storage[ProjectJob, ProjectJobID], abc.ABC):
    """
    Storage for project jobs.
    """
