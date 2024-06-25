import typing

from common.py.core.messaging import Channel, Message
from common.py.data.entities.authorization import AuthorizationToken
from common.py.data.entities.user import UserID

from .. import ServerServiceContext
from ...networking.session import Session


def get_user_authorizations(
    user_id: UserID, ctx: ServerServiceContext
) -> typing.List[str]:
    """
    Returns a list of all granted authorization IDs for the specified user.

    Args:
        user_id: The user ID.
        ctx: The service context.

    Returns:
        A list of all granted authorization IDs.
    """
    return list(
        map(
            lambda token: token.auth_id,
            ctx.storage_pool.authorization_token_storage.filter_by_user(user_id),
        )
    )


def send_user_authorizations(
    msg: Message,
    ctx: ServerServiceContext,
    *,
    session: Session | None = None,
) -> None:
    """
    Sends all granted authorizations to the currently authenticated user.

    Args:
        msg: Original message for chaining.
        ctx: The service context.
        session: Override the user ID and target to use using a user's session.
    """
    from common.py.api.user import UserAuthorizationsListEvent

    if ctx.user is None and (session or session.user_token) is None:
        raise RuntimeError("Sending user authorizations without an authenticated user")

    if (
        user := ctx.storage_pool.user_storage.get(
            session.user_token.user_id
            if session and session.user_token
            else ctx.user.user_id
        )
    ) is not None:
        UserAuthorizationsListEvent.build(
            ctx.message_builder,
            authorizations=get_user_authorizations(user.user_id, ctx),
            chain=msg,
        ).emit(Channel.direct(session.user_origin if session else msg.origin))


def handle_authorization_token_changes(
    auth_token: AuthorizationToken,
    msg: Message,
    ctx: ServerServiceContext,
) -> None:
    """
    Sends all updated data to the user the authorization token belongs to.

    Args:
        auth_token: The authorization token.
        msg: Original message.
        ctx: The service context.
    """
    for session in ctx.session_manager.find_user_sessions(auth_token.user_id):
        send_user_authorizations(msg, ctx, session=session)
