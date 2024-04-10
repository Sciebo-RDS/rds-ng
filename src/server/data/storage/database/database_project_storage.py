import threading
import typing

from sqlalchemy import Table
from sqlalchemy.orm import Session

from common.py.data.entities.project import Project, ProjectID
from common.py.data.entities.user import UserID
from common.py.data.storage import ProjectStorage

from .database_storage_accessor import DatabaseStorageAccessor


class DatabaseProjectStorage(ProjectStorage):
    """
    Database storage for projects.
    """

    _lock = threading.RLock()

    def __init__(self, session: Session, table: Table):
        super().__init__()

        self._session = session
        self._table = table

        self._accessor = DatabaseStorageAccessor[Project, ProjectID](
            Project, self._session, self._lock
        )

    def next_id(self) -> ProjectID:
        # TODO
        pass

    def add(self, entity: Project) -> None:
        self._accessor.add(entity)

    def remove(self, entity: Project) -> None:
        self._accessor.remove(entity)

    def get(self, key: ProjectID) -> Project | None:
        return self._accessor.get(key)

    def list(self) -> typing.List[Project]:
        return self._accessor.list()

    def filter_by_user(self, user_id: UserID) -> typing.List[Project]:
        # TODO
        pass
