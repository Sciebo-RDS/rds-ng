import abc

from .storage import Storage
from ..entities.user import User, UserID


class UserStorage(Storage[User, UserID], abc.ABC):
    """
    Storage for users.
    """
