from .client_service_context import ClientServiceContext
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
        ServerDisconnectedEvent,
        ClientConnectedEvent,
        ClientDisconnectedEvent,
        ClientConnectionErrorEvent,
    )
    from ..api.component import ComponentInformationEvent

    svc = comp.create_service("Network service")

    @svc.message_handler(PingCommand)
    def ping(msg: PingCommand, ctx: ServiceContext) -> None:
        ctx.logger.debug("Received PING", scope="network", payload=msg.payload)

        PingReply.build(ctx.message_builder, msg).emit()

    @svc.message_handler(PingReply)
    def ping_reply(msg: PingReply, ctx: ServiceContext) -> None:
        ctx.logger.debug("Received PING reply", scope="network", payload=msg.payload)

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

    @svc.message_handler(ServerDisconnectedEvent)
    def server_disconnected(msg: ServerDisconnectedEvent, ctx: ServiceContext) -> None:
        pass

    @svc.message_handler(ClientConnectedEvent)
    def client_connected(msg: ClientConnectedEvent, ctx: ServiceContext) -> None:
        pass

    @svc.message_handler(ClientDisconnectedEvent)
    def client_disconnected(msg: ClientDisconnectedEvent, ctx: ServiceContext) -> None:
        ClientServiceContext.set_remote_channel(None)

    @svc.message_handler(ClientConnectionErrorEvent)
    def client_connection_error(
        msg: ClientConnectionErrorEvent, ctx: ServiceContext
    ) -> None:
        ClientServiceContext.set_remote_channel(None)

    return svc
