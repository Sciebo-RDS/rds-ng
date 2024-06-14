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

    from common.py.api import RevokeAuthorizationCommand, RevokeAuthorizationReply

    from .connector_service_context import ConnectorServiceContext

    svc = comp.create_service(
        "Authorization service", context_type=ConnectorServiceContext
    )

    @svc.message_handler(RevokeAuthorizationCommand, is_async=False)
    def revoke_authorization(
        msg: RevokeAuthorizationCommand, ctx: ConnectorServiceContext
    ):
        # We just forward the message to the server
        RevokeAuthorizationCommand.build(
            ctx.message_builder,
            user_id=msg.user_id,
            auth_id=msg.auth_id,
        ).failed(lambda _, err: None).emit(ctx.remote_channel)

        RevokeAuthorizationReply.build(
            ctx.message_builder,
            msg,
        ).emit()

    @svc.message_handler(RevokeAuthorizationReply, is_async=False)
    def revoke_authorization_reply(
        msg: RevokeAuthorizationReply, ctx: ConnectorServiceContext
    ):
        # Suppress warnings about this message not being handled
        pass

    return svc
