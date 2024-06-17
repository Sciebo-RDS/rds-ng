import threading
import typing

from sqlalchemy import Table, select
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
        from sqlalchemy import func

        statement = select(func.max(self._table.c.project_id))
        if (proj_id := self._session.execute(statement).scalar_one()) is not None:
            return typing.cast(ProjectID, proj_id + 1)

        return 1

    def add(self, entity: Project) -> None:
        self._accessor.add(entity)

    def remove(self, entity: Project) -> None:
        self._accessor.remove(entity)

    def get(self, key: ProjectID) -> Project | None:
        return self._accessor.get(key)

    def list(self) -> typing.List[Project]:
        return self._accessor.list()

    def filter_by_user(self, user_id: UserID) -> typing.List[Project]:
        return self._accessor.filter(self._table.c.user_id == user_id)
