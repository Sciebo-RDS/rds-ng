import threading
import typing

from sqlalchemy import Table
from sqlalchemy.orm import Session

from common.py.data.entities.user import UserID, User
from common.py.data.storage import UserStorage

from .database_storage_accessor import DatabaseStorageAccessor


class DatabaseUserStorage(UserStorage):
    """
    Database storage for users.
    """

    _lock = threading.RLock()

    def __init__(self, session: Session, table: Table):
        super().__init__()

        self._session = session
        self._table = table

        self._accessor = DatabaseStorageAccessor[User, UserID](
            User, self._session, self._lock
        )

    def next_id(self) -> UserID:
        raise NotImplementedError("Users do not support automatic IDs")

    def add(self, entity: User) -> None:
        self._accessor.add(entity)

    def remove(self, entity: User) -> None:
        self._accessor.remove(entity)

    def get(self, key: UserID) -> User | None:
        return self._accessor.get(key)

    def list(self) -> typing.List[User]:
        return self._accessor.list()
