import abc
import typing

from .storage import Storage
from ..entities.project import Project, ProjectID
from ..entities.user import UserID


class ProjectStorage(Storage[Project, ProjectID], abc.ABC):
    """
    Storage for projects.
    """

    @abc.abstractmethod
    def filter_by_user(self, user_id: UserID) -> typing.List[Project]:
        """
        Returns projects associated with the specified user.

        Args:
            user_id: The user ID.

        Returns:
            The matching projects list.
        """
