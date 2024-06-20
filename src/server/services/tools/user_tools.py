from common.py.core.messaging import Channel, Message
from common.py.data.entities import clone_entity
from common.py.data.entities.authorization import (
    AuthorizationState,
    AuthorizationToken,
)
from common.py.data.entities.user import User

from .. import ServerServiceContext
from ...networking.session import Session


def reflect_user_settings_authorization_states(
    ctx: ServerServiceContext, settings: User.Settings
) -> User.Settings:
    """
    Returns a copy of the user settings with all connector instances updated to reflect their authorization states

    Args:
        ctx: The message context.
        settings: The current user settings.

    Returns:
        The updated user settings.
    """
    # Update all connector instances to reflect their authorization state
    auth_tokens = ctx.storage_pool.authorization_token_storage.filter_by_user(
        ctx.user.user_id
    )

    settings = clone_entity(settings)
    for instance in settings.connector_instances:
        instance.authorization_state = AuthorizationState.NOT_AUTHORIZED
        for auth_token in auth_tokens:
            if (
                auth_token.auth_type == AuthorizationToken.TokenType.CONNECTOR
                and auth_token.auth_issuer == str(instance.instance_id)
            ):
                instance.authorization_state = AuthorizationState.AUTHORIZED

    return settings


def send_user_settings(
    msg: Message,
    ctx: ServerServiceContext,
    *,
    session: Session | None = None,
) -> None:
    """
    Sends the user settings to the currently authenticated user.

    Args:
        msg: Original message for chaining.
        ctx: The service context.
        session: Override the user ID and target to use using a user's session.
    """
    from common.py.api.user import UserSettingsChangedEvent

    if ctx.user is None and (session or session.user_token) is None:
        raise RuntimeError("Sending user settings without an authenticated user")

    if (
        user := ctx.storage_pool.user_storage.get(
            session.user_token.user_id
            if session and session.user_token
            else ctx.user.user_id
        )
    ) is not None:
        UserSettingsChangedEvent.build(
            ctx.message_builder,
            settings=reflect_user_settings_authorization_states(
                ctx, user.user_settings
            ),
            chain=msg,
        ).emit(Channel.direct(session.user_origin if session else msg.origin))


def handle_authorization_token_changes(
    auth_token: AuthorizationToken,
    msg: Message,
    ctx: ServerServiceContext,
) -> None:
    """
    Sends the updated settings to the user the authorization token belongs to.

    Args:
        auth_token: The authorization token.
        msg: Original message.
        ctx: The service context.
    """
    if (
        session := ctx.session_manager.find_user_session(auth_token.user_id)
    ) is not None:
        send_user_settings(msg, ctx, session=session)
