import typing

from sqlalchemy import Engine, Table

from common.py.data.entities.user import UserID, User
from common.py.data.storage import UserStorage


class DatabaseUserStorage(UserStorage):
    """
    Database storage for users.
    """

    def __init__(self, engine: Engine, table: Table):
        super().__init__()

        self._engine = engine
        self._table = table

    def next_id(self) -> UserID:
        raise NotImplementedError("Users do not support automatic IDs")

    def add(self, entity: User) -> None:
        pass

    def remove(self, entity: User) -> None:
        pass

    def get(self, key: UserID) -> User | None:
        pass

    def list(self) -> typing.List[User]:
        pass
