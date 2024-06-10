import threading
import typing

from common.py.data.entities.authorization import (
    AuthorizationToken,
    AuthorizationTokenID,
)
from common.py.data.entities.user import UserID
from common.py.data.storage import AuthorizationTokenStorage


class MemoryAuthorizationTokenStorage(AuthorizationTokenStorage):
    """
    In-memory storage for authorization tokens.
    """

    _tokens: typing.Dict[AuthorizationTokenID, AuthorizationToken] = {}
    _lock = threading.RLock()

    def next_id(self) -> AuthorizationTokenID:
        raise NotImplementedError("Authorization tokens do not support automatic IDs")

    def add(self, entity: AuthorizationToken) -> None:
        with MemoryAuthorizationTokenStorage._lock:
            MemoryAuthorizationTokenStorage._tokens[self._key_from_entity(entity)] = (
                entity
            )

    def remove(self, entity: AuthorizationToken) -> None:
        with MemoryAuthorizationTokenStorage._lock:
            try:
                del MemoryAuthorizationTokenStorage._tokens[
                    self._key_from_entity(entity)
                ]
            except Exception as exc:  # pylint: disable=broad-exception-caught
                from common.py.data.storage import StorageException

                raise StorageException(
                    f"An authorization token with ID {self._key_from_entity(entity)} was not found"
                ) from exc

    def get(self, key: AuthorizationTokenID) -> AuthorizationToken | None:
        with MemoryAuthorizationTokenStorage._lock:
            return (
                MemoryAuthorizationTokenStorage._tokens[key]
                if key in MemoryAuthorizationTokenStorage._tokens
                else None
            )

    def list(self) -> typing.List[AuthorizationToken]:
        with MemoryAuthorizationTokenStorage._lock:
            return list(MemoryAuthorizationTokenStorage._tokens.values())

    def filter_by_user(self, user_id: UserID) -> typing.List[AuthorizationToken]:
        with MemoryAuthorizationTokenStorage._lock:
            return list(
                filter(
                    lambda token: token.user_id == user_id,
                    MemoryAuthorizationTokenStorage._tokens.values(),
                )
            )

    def _key_from_entity(self, entity: AuthorizationToken) -> AuthorizationTokenID:
        return entity.user_id, entity.token_id
