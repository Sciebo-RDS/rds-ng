import threading
import typing

from sqlalchemy import Table
from sqlalchemy.orm import Session

from common.py.data.entities.project import ProjectJob, ProjectJobID, ProjectID
from common.py.data.storage import ProjectJobStorage

from .database_storage_accessor import DatabaseStorageAccessor


class DatabaseProjectJobStorage(ProjectJobStorage):
    """
    Database storage for project jobs.
    """

    _lock = threading.RLock()

    def __init__(self, session: Session, table: Table):
        super().__init__()

        self._session = session
        self._table = table

        self._accessor = DatabaseStorageAccessor[ProjectJob, ProjectJobID](
            ProjectJob, self._session, self._lock
        )

    def next_id(self) -> ProjectJobID:
        raise NotImplementedError("Project jobs do not support automatic IDs")

    def add(self, entity: ProjectJob) -> None:
        self._accessor.add(entity)

    def remove(self, entity: ProjectJob) -> None:
        self._accessor.remove(entity)

    def get(self, key: ProjectJobID) -> ProjectJob | None:
        return self._accessor.get(key)

    def list(self) -> typing.List[ProjectJob]:
        return self._accessor.list()

    def filter_by_project(self, project_id: ProjectID) -> typing.List[ProjectJob]:
        return self._accessor.filter(self._table.c.project_id == project_id)
