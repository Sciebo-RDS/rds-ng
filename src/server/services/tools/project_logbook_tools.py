import typing

from common.py.core.messaging import Message, Channel
from common.py.data.entities.project import Project
from common.py.data.entities.project.logbook import (
    ProjectLogbookRecord,
    ProjectLogbookType,
)

from .. import ServerServiceContext
from ...networking.session import Session


def send_project_logbook(
    msg: Message,
    ctx: ServerServiceContext,
    project: Project,
    *,
    session: Session | None = None,
) -> None:
    """
    Sends the logbook of a project to the currently authenticated user.

    Args:
        msg: Original message for chaining.
        ctx: The service context.
        project: The project.
        session: Override the user ID and target to use using a user's session.
    """
    from common.py.api.project import ProjectLogbookEvent

    if ctx.user is None and (session or session.user_token) is None:
        raise RuntimeError("Sending project logbook without an authenticated user")

    ProjectLogbookEvent.build(
        ctx.message_builder,
        project_id=project.project_id,
        logbook=project.logbook,
        chain=msg,
    ).emit(Channel.direct(session.user_origin if session else msg.origin))


def get_project_logbook(
    project: Project, logbook_type: ProjectLogbookType
) -> typing.List[ProjectLogbookRecord]:
    """
    Gets the logbook with the specified type of a project.

    Args:
        project: The project.
        logbook_type: The logbook type.

    Returns:
        The project logbook (contents); if the logbook doesn't exist, an empty list is returned.
    """
    if logbook_type == ProjectLogbookType.JOB_HISTORY:
        return project.logbook.job_history

    return typing.cast(typing.List[ProjectLogbookRecord], [])
