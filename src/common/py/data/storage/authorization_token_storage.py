import abc
import typing

from .storage import Storage
from ..entities.authorization import AuthorizationToken, AuthorizationTokenID
from ..entities.user import UserID


class AuthorizationTokenStorage(
    Storage[AuthorizationToken, AuthorizationTokenID], abc.ABC
):
    """
    Storage for authorization tokens.
    """

    @abc.abstractmethod
    def filter_by_user(self, user_id: UserID) -> typing.List[AuthorizationToken]:
        """
        Returns all tokens belonging to the specified user.

        Args:
            user_id: The user ID.

        Returns:
            The matching tokens list.
        """
