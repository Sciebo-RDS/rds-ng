import typing

from common.py.data.entities import Project, ProjectID
from common.py.data.storage import ProjectStorage


class MemoryProjectStorage(ProjectStorage):
    """
    In-memory storage for projects.
    """

    _projects: typing.Dict[ProjectID, Project] = {}

    def add(self, entity: Project) -> None:
        with self._lock:
            MemoryProjectStorage._projects[entity.project_id] = entity

    def remove(self, entity: Project) -> None:
        with self._lock:
            entity.status = Project.Status.DELETED

            try:
                del MemoryProjectStorage._projects[entity.project_id]
            except Exception as exc:  # pylint: disable=broad-exception-caught
                from common.py.data.storage import StorageException

                raise StorageException(
                    f"A project with ID {entity.project_id} was not found"
                ) from exc

    def get(self, key: ProjectID) -> Project | None:
        with self._lock:
            if key in MemoryProjectStorage._projects:
                return MemoryProjectStorage._projects[key]
            return None

    def list(self) -> typing.List[Project]:
        with self._lock:
            return list(MemoryProjectStorage._projects.values())
