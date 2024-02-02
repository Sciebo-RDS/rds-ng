import dataclasses
import threading
import typing

from common.py.data.entities.project import Project, ProjectID
from common.py.data.storage import ProjectStorage


class MemoryProjectStorage(ProjectStorage):
    """
    In-memory storage for projects.

    Args:
        storage_id: If set, the session storage is used instead of the global one.
    """

    default_projects: typing.List[Project] = []

    _global_projects: typing.Dict[str, typing.Dict[ProjectID, Project]] = {}

    _lock = threading.RLock()

    def __init__(self, storage_id: str):
        super().__init__()

        self._storage_id = storage_id

        has_storage = self._storage_id in MemoryProjectStorage._global_projects
        if not has_storage:
            MemoryProjectStorage._global_projects[storage_id] = {}

        self._projects = MemoryProjectStorage._global_projects[storage_id]

        if not has_storage:
            from common.py.data.entities import clone_entity

            for project in MemoryProjectStorage.default_projects:
                self.add(clone_entity(project))

    def next_id(self) -> ProjectID:
        with MemoryProjectStorage._lock:
            ids = self._projects.keys()
            if len(ids) > 0:
                return max(ids) + 1
            else:
                return 1000

    def add(self, entity: Project) -> None:
        with MemoryProjectStorage._lock:
            self._projects[entity.project_id] = entity

    def remove(self, entity: Project) -> None:
        with MemoryProjectStorage._lock:
            from common.py.data.entities import clone_entity

            proj_deleted = clone_entity(entity, status=Project.Status.DELETED)
            self.add(proj_deleted)

            try:
                del self._projects[entity.project_id]
            except Exception as exc:  # pylint: disable=broad-exception-caught
                from common.py.data.storage import StorageException

                raise StorageException(
                    f"A project with ID {entity.project_id} was not found"
                ) from exc

    def get(self, key: ProjectID) -> Project | None:
        with MemoryProjectStorage._lock:
            if key in self._projects:
                return self._projects[key]
            return None

    def list(self) -> typing.List[Project]:
        with MemoryProjectStorage._lock:
            return list(self._projects.values())
