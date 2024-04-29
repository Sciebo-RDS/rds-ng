from common.py.core.messaging import Message, Channel

from .. import ServerServiceContext
from ...networking.session import Session


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
