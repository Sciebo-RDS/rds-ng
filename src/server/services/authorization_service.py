from common.py.component import BackendComponent
from common.py.core import logging
from common.py.data.entities.authorization import (
    has_authorization_token_expired,
    get_host_authorization_token_id,
)
from common.py.data.verifiers.authorization import AuthorizationTokenVerifier
from common.py.integration.authorization.strategies import (
    create_authorization_strategy,
    AuthorizationStrategy,
)
from common.py.services import Service
from common.py.utils import EntryGuard


def create_authorization_service(comp: BackendComponent) -> Service:
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
    )
    from common.py.api.component import ComponentProcessEvent

    from .server_service_context import ServerServiceContext

    svc = comp.create_service(
        "Authorization service", context_type=ServerServiceContext
    )

    def _create_auth_strategy(
        ctx: ServerServiceContext, strategy: str
    ) -> AuthorizationStrategy:
        auth_token = (
            ctx.storage_pool.authorization_token_storage.get(
                get_host_authorization_token_id(ctx.user)
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
        )

    @svc.message_handler(RequestAuthorizationCommand)
    def request_authorization(
        msg: RequestAuthorizationCommand, ctx: ServerServiceContext
    ):
        if not ctx.ensure_user(msg, RequestAuthorizationReply):
            return

        success = False
        message = ""

        if msg.payload.fingerprint == ctx.session.fingerprint:
            try:
                strategy = _create_auth_strategy(ctx, msg.strategy)
                auth_token = strategy.request_authorization(
                    ctx.user.user_id,
                    msg.payload,
                    msg.data,
                )
                AuthorizationTokenVerifier(auth_token).verify_create()

                ctx.storage_pool.authorization_token_storage.add(auth_token)

                success = True
            except Exception as exc:  # pylint: disable=broad-exception-caught
                message = str(exc)
        else:
            message = "The provided fingerprint doesn't match"

        RequestAuthorizationReply.build(
            ctx.message_builder,
            msg,
            success=success,
            message=message,
        ).emit()

    @svc.message_handler(RevokeAuthorizationCommand, is_async=False)
    def revoke_authorization(
        msg: RevokeAuthorizationCommand, ctx: ServerServiceContext
    ):
        success = False
        message = ""

        if (
            auth_token := ctx.storage_pool.authorization_token_storage.get(
                (msg.user_id, msg.auth_id)
            )
        ) is not None:
            ctx.storage_pool.authorization_token_storage.remove(auth_token)

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

    @svc.message_handler(RevokeAuthorizationReply, is_async=False)
    def revoke_authorization_reply(
        msg: RevokeAuthorizationReply, ctx: ServerServiceContext
    ):
        # Suppress warnings about this message not being handled
        pass

    @svc.message_handler(ComponentProcessEvent)
    def refresh_expired_tokens(
        msg: ComponentProcessEvent, ctx: ServerServiceContext
    ) -> None:
        with EntryGuard("refresh_expired_tokens") as guard:
            if not guard.can_execute:
                return

            for auth_token in ctx.storage_pool.authorization_token_storage.list():
                if has_authorization_token_expired(auth_token):
                    try:
                        AuthorizationTokenVerifier(auth_token).verify_update()

                        strategy = _create_auth_strategy(ctx, auth_token.strategy)
                        strategy.refresh_authorization(auth_token)

                        logging.debug(
                            "Refreshed authorization token",
                            scope="authorization",
                            user_id=auth_token.user_id,
                            auth_id=auth_token.auth_id,
                            strategy=auth_token.strategy,
                        )
                    except Exception as exc:  # pylint: disable=broad-exception-caught
                        logging.warning(
                            "Unable to refresh authorization token - removing token",
                            scope="authorization",
                            user_id=auth_token.user_id,
                            auth_id=auth_token.auth_id,
                            strategy=auth_token.strategy,
                            error=str(exc),
                        )

                        ctx.storage_pool.authorization_token_storage.remove(auth_token)

    return svc
