import abc
import typing

from .storage import Storage
from ..entities.project import ProjectJob, ProjectJobID, ProjectID


class ProjectJobStorage(Storage[ProjectJob, ProjectJobID], abc.ABC):
    """
    Storage for project jobs.
    """

    @abc.abstractmethod
    def filter_by_project(self, project_id: ProjectID) -> typing.List[ProjectJob]:
        """
        Returns projects associated with the specified user.

        Args:
            project_id: The project ID.

        Returns:
            The matching project jobs list.
        """
