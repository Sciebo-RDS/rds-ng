import contextlib
import time

from common.py.component import BackendComponent
from common.py.core import logging
from common.py.data.entities.authorization import has_authorization_token_expired
from common.py.data.verifiers.authorization import AuthorizationTokenVerifier
from common.py.integration.authorization.strategies import (
    create_authorization_strategy,
    AuthorizationStrategy,
)
from common.py.services import Service
from common.py.utils.entry_guard import EntryGuard

from ..integration.authorization.strategies import get_strategy_configuration


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
    )
    from common.py.api.component import ComponentProcessEvent

    from .server_service_context import ServerServiceContext

    svc = comp.create_service(
        "Authorization service", context_type=ServerServiceContext
    )

    def _create_strategy(strategy: str) -> AuthorizationStrategy:
        return create_authorization_strategy(
            comp,
            svc,
            strategy,
            get_strategy_configuration(strategy),
        )

    @svc.message_handler(RequestAuthorizationCommand, is_async=True)
    def request_authorization(
        msg: RequestAuthorizationCommand, ctx: ServerServiceContext
    ):
        if not ctx.ensure_user(msg, RequestAuthorizationReply):
            return

        success = False
        message = ""

        if msg.fingerprint == ctx.session.fingerprint:
            try:
                strategy = _create_strategy(msg.strategy)
                auth_token = strategy.request_authorization(
                    ctx.user.user_id, msg.auth_id, msg.data
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

    @svc.message_handler(ComponentProcessEvent, is_async=True)
    def refresh_expired_tokens(
        msg: ComponentProcessEvent, ctx: ServerServiceContext
    ) -> None:
        with EntryGuard("refresh_expired_tokens") as guard:
            if not guard.can_execute:
                return

            for token in ctx.storage_pool.authorization_token_storage.list():
                if has_authorization_token_expired(token):
                    try:
                        token = ctx.storage_pool.authorization_token_storage.get(
                            (token.user_id, token.auth_id)
                        )
                        AuthorizationTokenVerifier(token).verify_update()

                        strategy = _create_strategy(token.strategy)
                        strategy.refresh_authorization(token)

                        logging.debug(
                            "Refreshed authorization token",
                            scope="authorization",
                            user_id=token.user_id,
                            auth_id=token.auth_id,
                            strategy=token.strategy,
                        )
                    except Exception as exc:  # pylint: disable=broad-exception-caught
                        logging.warning(
                            "Unable to refresh authorization token - removing token",
                            scope="authorization",
                            user_id=token.user_id,
                            auth_id=token.auth_id,
                            strategy=token.strategy,
                            error=str(exc),
                        )

                        ctx.storage_pool.authorization_token_storage.remove(token)

    return svc
