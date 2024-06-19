from common.py.data.entities.authorization import (
    AuthorizationState,
    AuthorizationToken,
)
from common.py.data.entities.user import User

from .. import ServerServiceContext


def reflect_user_settings_authorization_states(
    ctx: ServerServiceContext, settings: User.Settings
) -> None:
    # Update all connector instances to reflect their authorization state
    auth_tokens = ctx.storage_pool.authorization_token_storage.filter_by_user(
        ctx.user.user_id
    )

    for instance in settings.connector_instances:
        instance.authorization_state = AuthorizationState.NOT_AUTHORIZED
        for auth_token in auth_tokens:
            if (
                auth_token.auth_type == AuthorizationToken.TokenType.CONNECTOR
                and auth_token.auth_issuer == str(instance.instance_id)
            ):
                instance.authorization_state = AuthorizationState.AUTHORIZED
