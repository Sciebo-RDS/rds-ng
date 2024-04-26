import typing

from common.py.core.messaging import Message, Channel
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


def send_project_jobs_list(msg: Message, ctx: ServerServiceContext) -> None:
    """
    Sends the project job list to the currently authenticated user.

    Args:
        msg: Original message for chaining.
        ctx: The service context.
    """
    from common.py.api.project import JobsListEvent

    if ctx.user is None:
        raise RuntimeError("Sending project jobs list without an authenticated user")

    JobsListEvent.build(
        ctx.message_builder,
        project_jobs=get_user_project_jobs(ctx),
        chain=msg,
    ).emit(Channel.direct(msg.origin))
