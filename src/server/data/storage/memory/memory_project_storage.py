import typing

from common.py.data.entities.project import Project, ProjectID
from common.py.data.entities.user import UserID
from common.py.data.storage import ProjectStorage


class MemoryProjectStorage(ProjectStorage):
    """
    In-memory storage for projects.
    """

    def __init__(self):
        super().__init__()

        self._projects: typing.Dict[ProjectID, Project] = {}

    def next_id(self) -> ProjectID:
        with self._lock:
            ids = self._projects.keys()
            if len(ids) > 0:
                return max(ids) + 1
            else:
                return 1000

    def add(self, entity: Project) -> None:
        with self._lock:
            self._projects[entity.project_id] = entity

    def remove(self, entity: Project) -> None:
        with self._lock:
            try:
                del self._projects[entity.project_id]
            except Exception as exc:  # pylint: disable=broad-exception-caught
                from common.py.data.storage import StorageException

                raise StorageException(
                    f"A project with ID {entity.project_id} was not found"
                ) from exc

    def get(self, key: ProjectID) -> Project | None:
        with self._lock:
            return self._projects[key] if key in self._projects else None

    def list(self) -> typing.List[Project]:
        with self._lock:
            return list(self._projects.values())

    def filter_by_user(self, user_id: UserID) -> typing.List[Project]:
        with self._lock:
            return list(
                filter(lambda proj: proj.user_id == user_id, self._projects.values())
            )
