import typing

from common.py.core.messaging import Message, Channel
from common.py.data.entities.project import ProjectJobID, ProjectJob

from .. import ServerServiceContext
from ...networking.session import Session

ModifyProjectJobCallback = typing.Callable[[ProjectJob], None]


def send_project_jobs_list(
    msg: Message,
    ctx: ServerServiceContext,
    *,
    session: Session | None = None,
) -> None:
    """
    Sends the project job list to the currently authenticated user.

    Args:
        msg: Original message for chaining.
        ctx: The service context.
        session: Override the user ID and target to use using a user's session.
    """
    from common.py.api.project import ProjectJobsListEvent

    if ctx.user is None and (session or session.user_token) is None:
        raise RuntimeError("Sending project jobs list without an authenticated user")

    ProjectJobsListEvent.build(
        ctx.message_builder,
        jobs=ctx.storage_pool.project_job_storage.filter_by_user(
            session.user_token.user_id
            if session and session.user_token
            else ctx.user.user_id
        ),
        chain=msg,
    ).emit(Channel.direct(session.user_origin if session else msg.origin))


def modify_project_job(
    job_id: ProjectJobID,
    callback: ModifyProjectJobCallback,
    msg: Message,
    ctx: ServerServiceContext,
) -> None:
    """
    Modifies a project job via a callback and sends the updated jobs list to the user.

    Args:
        job_id: The job ID.
        callback: The callback function.
        msg: Original message.
        ctx: The service context.
    """
    if (job := ctx.storage_pool.project_job_storage.get(job_id)) is not None:
        callback(job)

        if (session := ctx.session_manager.find_user_session(job.user_id)) is not None:
            send_project_jobs_list(msg, ctx, session=session)
