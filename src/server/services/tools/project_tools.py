from common.py.core.messaging import Message, Channel

from .. import ServerServiceContext


def send_projects_list(msg: Message, ctx: ServerServiceContext) -> None:
    """
    Sends the project list to the currently authenticated user.

    Args:
        msg: Original message for chaining.
        ctx: The service context.
    """
    from common.py.api import ProjectsListEvent

    if ctx.user is None:
        raise RuntimeError("Sending projects list without an authenticated user")

    ProjectsListEvent.build(
        ctx.message_builder,
        projects=ctx.storage_pool.project_storage.filter_by_user(ctx.user.user_id),
        chain=msg,
    ).emit(Channel.direct(msg.origin))
