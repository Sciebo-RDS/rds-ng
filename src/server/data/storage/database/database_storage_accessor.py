import typing
from threading import RLock
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

EntityType = TypeVar("EntityType")  # pylint: disable=invalid-name
EntityKeyType = TypeVar("EntityKeyType")  # pylint: disable=invalid-name


class DatabaseStorageAccessor(typing.Generic[EntityType, EntityKeyType]):
    """
    A storage-like helper class to access database objects.
    """

    def __init__(self, entity_type: typing.Type, session: Session, lock: RLock):
        self._entity_type = entity_type
        self._session = session
        self._lock = lock

    def add(self, entity: EntityType) -> None:
        with self._lock:
            self._session.add(entity)

    def remove(self, entity: EntityType) -> None:
        with self._lock:
            self._session.delete(entity)

    def get(self, key: EntityKeyType) -> EntityType | None:
        with self._lock:
            return self._session.get(self._entity_type, key)

    def list(self) -> typing.List[EntityType]:
        with self._lock:
            return typing.cast(
                typing.List[EntityType],
                self._session.execute(select(self._entity_type)).scalars().all(),
            )
