import threading
import typing

from common.py.data.entities.project import Project, ProjectID
from common.py.data.entities.user import UserID
from common.py.data.storage import ProjectStorage


class MemoryProjectStorage(ProjectStorage):
    """
    In-memory storage for projects.
    """

    _projects: typing.Dict[ProjectID, Project] = {}
    _lock = threading.RLock()

    def next_id(self) -> ProjectID:
        with MemoryProjectStorage._lock:
            ids = MemoryProjectStorage._projects.keys()
            if len(ids) > 0:
                return max(ids) + 1
            else:
                return 1000

    def add(self, entity: Project) -> None:
        with MemoryProjectStorage._lock:
            MemoryProjectStorage._projects[entity.project_id] = entity

    def remove(self, entity: Project) -> None:
        with MemoryProjectStorage._lock:
            try:
                del MemoryProjectStorage._projects[entity.project_id]
            except Exception as exc:  # pylint: disable=broad-exception-caught
                from common.py.data.storage import StorageException

                raise StorageException(
                    f"A project with ID {entity.project_id} was not found"
                ) from exc

    def get(self, key: ProjectID) -> Project | None:
        with MemoryProjectStorage._lock:
            return (
                MemoryProjectStorage._projects[key]
                if key in MemoryProjectStorage._projects
                else None
            )

    def list(self) -> typing.List[Project]:
        with MemoryProjectStorage._lock:
            return list(MemoryProjectStorage._projects.values())

    def filter_by_user(self, user_id: UserID) -> typing.List[Project]:
        with MemoryProjectStorage._lock:
            return list(
                filter(
                    lambda proj: proj.user_id == user_id,
                    MemoryProjectStorage._projects.values(),
                )
            )
