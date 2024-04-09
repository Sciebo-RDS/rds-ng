import threading
import typing

from sqlalchemy import Engine

from common.py.data.entities.project import Project, ProjectID
from common.py.data.entities.user import UserID
from common.py.data.storage import ProjectStorage


class DatabaseProjectStorage(ProjectStorage):
    """
    Database storage for projects.
    """

    def __init__(self, engine: Engine):
        super().__init__()

        self._engine = engine

        self._lock = threading.RLock()

    def next_id(self) -> ProjectID:
        pass

    def add(self, entity: Project) -> None:
        pass

    def remove(self, entity: Project) -> None:
        pass

    def get(self, key: ProjectID) -> Project | None:
        pass

    def list(self) -> typing.List[Project]:
        pass

    def filter_by_user(self, user_id: UserID) -> typing.List[Project]:
        pass
