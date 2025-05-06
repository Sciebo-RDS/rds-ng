import typing

from common.py.core.messaging import Message, Channel
from common.py.data.entities.project import ProjectJobID, ProjectJob

from .. import ServerServiceContext
from ...networking.session import Session

ModifyProjectJobCallback = typing.Callable[[ProjectJob], None]
NotifyProjectJobCallback = typing.Callable[[ProjectJob, Session], None]


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
    msg: Message,
    ctx: ServerServiceContext,
    *,
    update_callback: ModifyProjectJobCallback | None = None,
    notify_callback: NotifyProjectJobCallback | None = None,
) -> None:
    """
    Modifies a project job via a callback and sends the updated jobs list to the user.

    Args:
        job_id: The job ID.
        update_callback: Callback function to update the job (called once).
        notify_callback: Callback function to notify users about the updated job (called per user session).
        msg: Original message.
        ctx: The service context.
    """
    if (job := ctx.storage_pool.project_job_storage.get(job_id)) is not None:
        if update_callback is not None:
            update_callback(job)

        for session in ctx.session_manager.find_user_sessions(job.user_id):
            if notify_callback is not None:
                notify_callback(job, session)

            send_project_jobs_list(msg, ctx, session=session)
