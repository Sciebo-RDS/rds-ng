import threading
import typing

from sqlalchemy import Table
from sqlalchemy.orm import Session

from common.py.data.entities.authorization import (
    AuthorizationToken,
    AuthorizationTokenID,
)
from common.py.data.entities.user import UserID
from common.py.data.storage import AuthorizationTokenStorage

from .database_storage_accessor import DatabaseStorageAccessor


class DatabaseAuthorizationTokenStorage(AuthorizationTokenStorage):
    """
    Database storage for authorization tokens.
    """

    _lock = threading.RLock()

    def __init__(self, session: Session, table: Table):
        super().__init__()

        self._session = session
        self._table = table

        self._accessor = DatabaseStorageAccessor[
            AuthorizationToken, AuthorizationTokenID
        ](AuthorizationToken, self._session, self._lock)

    def next_id(self) -> AuthorizationTokenID:
        raise NotImplementedError("Authorization tokens do not support automatic IDs")

    def add(self, entity: AuthorizationToken) -> None:
        self._accessor.add(entity)

    def remove(self, entity: AuthorizationToken) -> None:
        self._accessor.remove(entity)

    def get(self, key: AuthorizationTokenID) -> AuthorizationToken | None:
        return self._accessor.get(key)

    def list(self) -> typing.List[AuthorizationToken]:
        return self._accessor.list()

    def filter_by_user(self, user_id: UserID) -> typing.List[AuthorizationToken]:
        return self._accessor.filter(self._table.c.user_id == user_id)
