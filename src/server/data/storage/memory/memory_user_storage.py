import threading
import typing

from common.py.data.entities.user import UserID, User
from common.py.data.storage import UserStorage


class MemoryUserStorage(UserStorage):
    """
    In-memory storage for projects.
    """

    _global_users: typing.Dict[UserID, User] = {}

    _lock = threading.RLock()

    def __init__(self):
        super().__init__()

        self._users = MemoryUserStorage._global_users

    def next_id(self) -> UserID:
        raise NotImplementedError("Users do not support automatic IDs")

    def add(self, entity: User) -> None:
        with MemoryUserStorage._lock:
            self._users[entity.user_id] = entity

    def remove(self, entity: User) -> None:
        with MemoryUserStorage._lock:

            try:
                del self._users[entity.user_id]
            except Exception as exc:  # pylint: disable=broad-exception-caught
                from common.py.data.storage import StorageException

                raise StorageException(
                    f"A user with ID {entity.user_id} was not found"
                ) from exc

    def get(self, key: UserID) -> User | None:
        with MemoryUserStorage._lock:
            if key in self._users:
                return self._users[key]
            return None

    def list(self) -> typing.List[User]:
        with MemoryUserStorage._lock:
            return list(self._users.values())
