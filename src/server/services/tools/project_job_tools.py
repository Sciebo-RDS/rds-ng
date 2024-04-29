from common.py.core.messaging import Message, Channel

from .. import ServerServiceContext


def send_project_jobs_list(msg: Message, ctx: ServerServiceContext) -> None:
    """
    Sends the project job list to the currently authenticated user.

    Args:
        msg: Original message for chaining.
        ctx: The service context.
    """
    from common.py.api.project import ProjectJobsListEvent

    if ctx.user is None:
        raise RuntimeError("Sending project jobs list without an authenticated user")

    ProjectJobsListEvent.build(
        ctx.message_builder,
        jobs=ctx.storage_pool.project_job_storage.filter_by_user(ctx.user.user_id),
        chain=msg,
    ).emit(Channel.direct(msg.origin))
