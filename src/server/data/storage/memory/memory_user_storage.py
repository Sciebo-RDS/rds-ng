import threading
import typing

from common.py.data.entities.user import UserID, User
from common.py.data.storage import UserStorage


class MemoryUserStorage(UserStorage):
    """
    In-memory storage for users.
    """

    _users: typing.Dict[UserID, User] = {}
    _lock = threading.RLock()

    def next_id(self) -> UserID:
        raise NotImplementedError("Users do not support automatic IDs")

    def add(self, entity: User) -> None:
        with MemoryUserStorage._lock:
            MemoryUserStorage._users[entity.user_id] = entity

    def remove(self, entity: User) -> None:
        with MemoryUserStorage._lock:
            try:
                del MemoryUserStorage._users[entity.user_id]
            except Exception as exc:  # pylint: disable=broad-exception-caught
                from common.py.data.storage import StorageException

                raise StorageException(
                    f"A user with ID {entity.user_id} was not found"
                ) from exc

    def get(self, key: UserID) -> User | None:
        with MemoryUserStorage._lock:
            return (
                MemoryUserStorage._users[key]
                if key in MemoryUserStorage._users
                else None
            )

    def list(self) -> typing.List[User]:
        with MemoryUserStorage._lock:
            return list(MemoryUserStorage._users.values())
