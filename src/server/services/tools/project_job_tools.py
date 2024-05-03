import typing

from common.py.core.messaging import Message, Channel
from common.py.data.entities.project import ProjectJobID, ProjectJob

from .. import ServerServiceContext
from ...networking.session import Session

ModifyProjectJobCallback = typing.Callable[[ProjectJob, Session | None], None]


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


def handle_project_job_message(
    job_id: ProjectJobID,
    callback: ModifyProjectJobCallback,
    msg: Message,
    ctx: ServerServiceContext,
    *,
    send_jobs: bool = True,
) -> None:
    """
    Modifies a project job via a callback and sends the updated jobs list to the user.

    Args:
        job_id: The job ID.
        callback: The callback function.
        msg: Original message.
        ctx: The service context.
        send_jobs: Whether to send the project jobs list to the user.
    """
    if (job := ctx.storage_pool.project_job_storage.get(job_id)) is not None:
        session = ctx.session_manager.find_user_session(job.user_id)

        callback(job, session)

        if session is not None:
            if send_jobs:
                send_project_jobs_list(msg, ctx, session=session)
