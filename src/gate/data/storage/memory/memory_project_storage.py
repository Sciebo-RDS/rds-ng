import typing

from common.py.data.entities import Project, ProjectID
from common.py.data.storage import ProjectStorage


class MemoryProjectStorage(ProjectStorage):
    """
    In-memory storage for projects.
    """

    _projects: typing.Dict[ProjectID, Project] = {}

    def add(self, project: Project) -> None:
        with self._lock:
            MemoryProjectStorage._projects[project.project_id] = project

    def remove(self, project: Project) -> None:
        with self._lock:
            try:
                del MemoryProjectStorage._projects[project.project_id]
            except:  # pylint: disable=bare-except
                from common.py.data.storage import StorageException

                raise StorageException(
                    f"A project with ID {project.project_id} was not found"
                )

    def get(self, key: ProjectID) -> Project | None:
        with self._lock:
            if key in MemoryProjectStorage._projects:
                return MemoryProjectStorage._projects[key]
            return None

    def list(self) -> typing.List[Project]:
        with self._lock:
            return list(MemoryProjectStorage._projects.values())
