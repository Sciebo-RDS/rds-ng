import typing

from .. import ProjectStorage
from ...entities.project import ProjectID, Project


class MemoryProjectStorage(ProjectStorage):
    """
    In-memory storage for projects.
    """

    _projects: typing.Dict[ProjectID, Project] = {}

    def add(self, project: Project) -> None:
        MemoryProjectStorage._projects[project.project_id] = project

    def remove(self, project: Project) -> None:
        try:
            del MemoryProjectStorage._projects[project.project_id]
        except:  # pylint: disable=bare-except
            from .. import StorageException

            raise StorageException(
                f"A project with ID {project.project_id} was not found"
            )

    def get(self, key: ProjectID) -> Project | None:
        if key in MemoryProjectStorage._projects:
            return MemoryProjectStorage._projects[key]
        return None

    def list(self) -> typing.List[Project]:
        return list(MemoryProjectStorage._projects.values())
