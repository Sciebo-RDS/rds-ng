import abc
import typing

from .storage import Storage
from ..entities.project import ProjectJob, ProjectJobID, ProjectID
from ..entities.user import UserID


class ProjectJobStorage(Storage[ProjectJob, ProjectJobID], abc.ABC):
    """
    Storage for project jobs.
    """

    @abc.abstractmethod
    def filter_by_user(self, user_id: UserID) -> typing.List[ProjectJob]:
        """
        Returns all jobs belonging to the specified user.

        Args:
            user_id: The user ID.

        Returns:
            The matching project jobs list.
        """

    @abc.abstractmethod
    def filter_by_project(self, project_id: ProjectID) -> typing.List[ProjectJob]:
        """
        Returns all jobs belonging to the specified project.

        Args:
            project_id: The project ID.

        Returns:
            The matching project jobs list.
        """
