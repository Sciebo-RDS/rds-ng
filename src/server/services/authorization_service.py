from common.py.component import BackendComponent
from common.py.services import Service


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

    @svc.message_handler(RequestAuthorizationCommand, is_async=True)
    def request_authorization(
        msg: RequestAuthorizationCommand, ctx: ServerServiceContext
    ):
        if not ctx.ensure_user(msg, RequestAuthorizationReply):
            return

        success = False
        message = ""

        if msg.fingerprint == ctx.session.fingerprint:
            # TODO: Secret in cfg: secrets.host
            success = True
        else:
            message = "The provided fingerprint doesn't match"

        RequestAuthorizationReply.build(
            ctx.message_builder,
            msg,
            success=success,
            message=message,
        ).emit()

    @svc.message_handler(ComponentProcessEvent)
    def process_authorization_tokens(
        msg: ComponentProcessEvent, ctx: ServerServiceContext
    ) -> None:
        pass

    return svc
