from .. import BackendComponent
from ...service import Service, ServiceContext
from ...utils import UnitID


def create_common_service(comp: BackendComponent) -> Service:
    """
    Creates the common service that handles various basic messaging tasks.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.

    """
    from ...core.messaging import Channel
    from ...api import (
        PingCommand,
        PingReply,
        ServerConnectedEvent,
        ComponentInformationEvent,
    )

    svc = comp.create_service("Common service")

    @svc.message_handler(PingCommand)
    def ping_command(msg: PingCommand, ctx: ServiceContext) -> None:
        ctx.logger.debug("Received PING", scope="component", payload=msg.payload)

        PingReply.emit(ctx.message_emitter, msg)

    @svc.message_handler(PingReply)
    def ping_reply(msg: PingReply, ctx: ServiceContext) -> None:
        ctx.logger.debug("Received PING reply", scope="component", payload=msg.payload)

    @svc.message_handler(ServerConnectedEvent)
    def server_connected(msg: ServerConnectedEvent, ctx: ServiceContext) -> None:
        # Whenever a client connects to our server, automatically send the server's component information
        _emit_comp_info(msg.comp_id, ctx)

    @svc.message_handler(ComponentInformationEvent)
    def component_information(
        msg: ComponentInformationEvent, ctx: ServiceContext
    ) -> None:
        from ...core.messaging.meta import MessageMetaInformation

        # If this message is received through the client, we need to send our information in return
        if ctx.meta_information.entrypoint == MessageMetaInformation.Entrypoint.CLIENT:
            _emit_comp_info(msg.comp_id, ctx)

    def _emit_comp_info(comp_id: UnitID, ctx: ServiceContext) -> None:
        data = BackendComponent.instance().data

        ComponentInformationEvent.emit(
            ctx.message_emitter,
            Channel.direct(comp_id),
            comp_id=data.comp_id,
            comp_name=data.name,
            comp_version=str(data.version),
        )

    return svc
