from .service import Service, ServiceContext
from ..component import BackendComponent


def create_network_service(comp: BackendComponent) -> Service:
    """
    Creates the network service that reacts to general networking-related messages.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.

    """
    from ..core.messaging import Channel
    from ..api.network import (
        PingCommand,
        PingReply,
        ServerConnectedEvent,
    )
    from ..api.component import ComponentInformationEvent

    svc = comp.create_service("Network service")

    @svc.message_handler(PingCommand)
    def ping(msg: PingCommand, ctx: ServiceContext) -> None:
        ctx.logger.debug("Received PING", scope="component", payload=msg.payload)

        PingReply.build(ctx.message_builder, msg).emit()

    @svc.message_handler(PingReply)
    def ping_reply(msg: PingReply, ctx: ServiceContext) -> None:
        ctx.logger.debug("Received PING reply", scope="component", payload=msg.payload)

    @svc.message_handler(ServerConnectedEvent)
    def server_connected(msg: ServerConnectedEvent, ctx: ServiceContext) -> None:
        # Whenever a client connects to our server, automatically send the server's component information
        data = BackendComponent.instance().data

        ComponentInformationEvent.build(
            ctx.message_builder,
            comp_id=data.comp_id,
            comp_name=data.name,
            comp_version=str(data.version),
            chain=msg,
        ).emit(Channel.direct(msg.comp_id))

    return svc
