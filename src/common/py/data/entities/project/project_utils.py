import typing

from .project import Project, ProjectID


def find_project_by_id(
    projects: typing.List[Project], project_id: ProjectID
) -> Project | None:
    """
    Searches for a project by its ID within a list of projects.

    Args:
        projects: The list of projects.
        project_id: The project to search for.

    Returns:
        The found project or **None** otherwise.
    """
    matching_project = (proj for proj in projects if proj.project_id == project_id)
    return next(matching_project, None)
