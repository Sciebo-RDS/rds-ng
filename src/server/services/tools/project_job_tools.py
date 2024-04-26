import typing

from common.py.data.entities.project import ProjectJob

from .. import ServerServiceContext


def get_user_project_jobs(ctx: ServerServiceContext) -> typing.List[ProjectJob]:
    """
    Gets all project jobs of a user.

    Args:
        ctx: The service context.

    Returns:
        List of all jobs of the user.
    """

    # Get all jobs for a user by first getting all his project, then getting all jobs associated with them
    project_jobs: typing.List[ProjectJob] = []
    for project in ctx.storage_pool.project_storage.filter_by_user(ctx.user.user_id):
        project_jobs.extend(
            ctx.storage_pool.project_job_storage.filter_by_project(project.project_id)
        )
    return project_jobs
