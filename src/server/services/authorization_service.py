import time

from common.py.core import logging
from common.py.data.entities.authorization import (
    AuthorizationSettings,
    AuthorizationToken,
    get_host_authorization_token_id,
    has_authorization_token_expired,
)
from common.py.data.verifiers.authorization import AuthorizationTokenVerifier
from common.py.integration.authorization.strategies import (
    AuthorizationStrategy,
    create_authorization_strategy,
)
from common.py.services import Service
from common.py.utils import EntryGuard
from common.py.utils.func import attempt

from .tools import handle_authorization_token_changes
from ..component import ServerComponent
from ..settings import AuthorizationSettingIDs


def create_authorization_service(comp: ServerComponent) -> Service:
    """
    Creates the authorization service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    from common.py.api.authorization import (
        RequestAuthorizationCommand,
        RequestAuthorizationReply,
        RevokeAuthorizationCommand,
        RevokeAuthorizationReply,
        GetAuthorizationTokenCommand,
        GetAuthorizationTokenReply,
    )
    from common.py.api.component import ComponentProcessEvent

    from .server_service_context import ServerServiceContext

    svc = comp.create_service(
        "Authorization service", context_type=ServerServiceContext
    )

    request_attempts_delay = comp.data.config.value(
        AuthorizationSettingIDs.REQUEST_ATTEMPTS_DELAY
    )
    request_attempts_limit = comp.data.config.value(
        AuthorizationSettingIDs.REQUEST_ATTEMPTS_LIMIT
    )
    refresh_attempts_delay = comp.data.config.value(
        AuthorizationSettingIDs.REFRESH_ATTEMPTS_DELAY
    )
    refresh_attempts_limit = comp.data.config.value(
        AuthorizationSettingIDs.REFRESH_ATTEMPTS_LIMIT
    )

    def _create_auth_strategy(
        ctx: ServerServiceContext,
        strategy: str,
        *,
        auth_token: AuthorizationToken | None = None,
        auth_public: AuthorizationSettings | None = None,
        auth_private: AuthorizationSettings | None = None,
    ) -> AuthorizationStrategy:
        if auth_token is None:
            auth_token = (
                ctx.storage_pool.authorization_token_storage.get(
                    get_host_authorization_token_id(ctx.user.user_id)
                )
                if ctx.user
                else None
            )

        return create_authorization_strategy(
            comp,
            svc,
            strategy,
            user_token=ctx.session.user_token if ctx.session else None,
            auth_token=auth_token,
            auth_public=auth_public,
            auth_private=auth_private,
        )

    @svc.message_handler(RequestAuthorizationCommand)
    def request_authorization(
        msg: RequestAuthorizationCommand, ctx: ServerServiceContext
    ) -> None:
        if not ctx.ensure_user(msg, RequestAuthorizationReply):
            return

        success = False
        message = ""

        if msg.request_payload.fingerprint == ctx.session.fingerprint:

            def _perform_auth() -> None:
                strategy = _create_auth_strategy(
                    ctx,
                    msg.strategy,
                    auth_public=ctx.public_auth_settings.get_settings(
                        msg.request_payload.auth_bearer
                    ),
                    auth_private=ctx.private_auth_settings.get_settings(
                        msg.request_payload.auth_bearer
                    ),
                )
                auth_token = strategy.request_authorization(
                    user_id=ctx.user.user_id,
                    host_id=(
                        ctx.user.host_id
                        if msg.request_payload.auth_type
                        == AuthorizationToken.TokenType.HOST
                        else None
                    ),  # The host ID is only relevant for host tokens
                    payload=msg.request_payload,
                    request_data=msg.data,
                )
                AuthorizationTokenVerifier(auth_token).verify_create()

                ctx.storage_pool.authorization_token_storage.add(auth_token)
                handle_authorization_token_changes(auth_token, msg, ctx)

                logging.debug(
                    f"Requested authorization token",
                    scope="auth",
                    user_id=auth_token.user_id,
                    auth_id=auth_token.auth_id,
                    strategy=auth_token.strategy,
                )

            def _perform_auth_failed(exc: Exception) -> None:
                nonlocal message
                message = str(exc)

                logging.warning(
                    "Requesting authorization failed",
                    scope="auth",
                    strategy=msg.strategy,
                    payload=msg.request_payload,
                    data=msg.data,
                    error=message,
                )

            success, _ = attempt(
                _perform_auth,
                cb_failed=_perform_auth_failed,
                attempts=request_attempts_limit,
                delay=request_attempts_delay,
            )
        else:
            message = "The provided fingerprint doesn't match"

        RequestAuthorizationReply.build(
            ctx.message_builder,
            msg,
            success=success,
            message=message,
        ).emit()

    @svc.message_handler(RevokeAuthorizationCommand)
    def revoke_authorization(
        msg: RevokeAuthorizationCommand, ctx: ServerServiceContext
    ) -> None:
        success = False
        message = ""

        if (user := ctx.user) is not None:
            user_id = user.user_id
        else:
            user_id = msg.user_id

        if (
            auth_token := ctx.storage_pool.authorization_token_storage.get(
                (user_id, msg.auth_id)
            )
        ) is not None:
            if msg.force:
                ctx.storage_pool.authorization_token_storage.remove(auth_token)
            else:
                # Invalidate the token, ensuring that a refresh will be tried (if possible)
                auth_token.state = AuthorizationToken.TokenState.INVALID
                auth_token.timestamp = time.time()
                auth_token.expiration_timestamp = (
                    1 if auth_token.expiration_timestamp else 0
                )
                auth_token.refresh_attempts = 0

            handle_authorization_token_changes(auth_token, msg, ctx)

            success = True
        else:
            message = (
                f"No authorization token {msg.auth_id} for user {msg.user_id} found"
            )

        RevokeAuthorizationReply.build(
            ctx.message_builder,
            msg,
            success=success,
            message=message,
        ).emit()

    @svc.message_handler(RevokeAuthorizationReply)
    def revoke_authorization_reply(
        msg: RevokeAuthorizationReply, ctx: ServerServiceContext
    ) -> None:
        # Suppress warnings about this message not being handled
        pass

    @svc.message_handler(GetAuthorizationTokenCommand)
    def get_authorization_token(
        msg: GetAuthorizationTokenCommand, ctx: ServerServiceContext
    ) -> None:
        auth_token = ctx.storage_pool.authorization_token_storage.get(
            (msg.user_id, msg.auth_id)
        )

        if (
            auth_token is None
            or auth_token.state != AuthorizationToken.TokenState.VALID
        ):
            auth_token = None

        GetAuthorizationTokenReply.build(
            ctx.message_builder,
            msg,
            auth_token=auth_token,
            api_key=ctx.api_key,
            success=auth_token is not None,
            message=(
                "No matching authorization token found" if auth_token is None else ""
            ),
        ).emit()

    @svc.message_handler(ComponentProcessEvent)
    def refresh_expired_tokens(
        msg: ComponentProcessEvent, ctx: ServerServiceContext
    ) -> None:
        with EntryGuard("refresh_expired_tokens") as guard:
            if not guard.can_execute:
                return

            def _attempt_refresh(token: AuthorizationToken) -> bool:
                return (
                    token.refresh_attempts == 0
                    or token.timestamp + refresh_attempts_delay <= time.time()
                )

            for auth_token in ctx.storage_pool.authorization_token_storage.list():
                if has_authorization_token_expired(auth_token) and _attempt_refresh(
                    auth_token
                ):
                    try:
                        AuthorizationTokenVerifier(auth_token).verify_update()

                        user = (
                            ctx.storage_pool.user_storage.get(auth_token.user_id)
                            if auth_token.auth_type == AuthorizationToken.TokenType.HOST
                            else None
                        )  # The host ID (fetched from the corresponding user account) is only relevant for host tokens

                        strategy = _create_auth_strategy(
                            ctx,
                            auth_token.strategy,
                            auth_token=auth_token,
                            auth_public=ctx.public_auth_settings.get_settings(
                                auth_token.auth_bearer
                            ),
                            auth_private=ctx.private_auth_settings.get_settings(
                                auth_token.auth_bearer
                            ),
                        )
                        strategy.refresh_authorization(
                            auth_token,
                            host_id=user.host_id if user is not None else None,
                        )

                        logging.debug(
                            "Refreshed authorization token",
                            scope="auth",
                            user_id=auth_token.user_id,
                            auth_id=auth_token.auth_id,
                            strategy=auth_token.strategy,
                        )
                    except Exception as exc:  # pylint: disable=broad-exception-caught
                        if 0 < refresh_attempts_limit <= auth_token.refresh_attempts:
                            logging.warning(
                                "Unable to refresh authorization token - removing token",
                                scope="auth",
                                user_id=auth_token.user_id,
                                auth_id=auth_token.auth_id,
                                strategy=auth_token.strategy,
                                error=str(exc),
                            )

                            ctx.storage_pool.authorization_token_storage.remove(
                                auth_token
                            )
                            handle_authorization_token_changes(auth_token, msg, ctx)

    return svc
