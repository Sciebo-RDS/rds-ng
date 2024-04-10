import typing

from common.py.data.entities.user import UserID, User
from common.py.data.storage import UserStorage


class MemoryUserStorage(UserStorage):
    """
    In-memory storage for users.
    """

    def __init__(self):
        super().__init__()

        self._users: typing.Dict[UserID, User] = {}

    def next_id(self) -> UserID:
        raise NotImplementedError("Users do not support automatic IDs")

    def add(self, entity: User) -> None:
        with self._lock:
            self._users[entity.user_id] = entity

    def remove(self, entity: User) -> None:
        with self._lock:
            try:
                del self._users[entity.user_id]
            except Exception as exc:  # pylint: disable=broad-exception-caught
                from common.py.data.storage import StorageException

                raise StorageException(
                    f"A user with ID {entity.user_id} was not found"
                ) from exc

    def get(self, key: UserID) -> User | None:
        with self._lock:
            return self._users[key] if key in self._users else None

    def list(self) -> typing.List[User]:
        with self._lock:
            return list(self._users.values())
