from .. import BackendComponent
from ...service import Service, ServiceContext
from ...utils import UnitID


class CommonServiceContext(ServiceContext):
    """
    Context type for the common service.
    """

    comp_info = {
        "comp_id": UnitID("", ""),
        "name": "",
        "version": "",
    }


def create_common_service(comp: BackendComponent) -> Service:
    """
    Creates the common service that handles various basic messaging tasks.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.

    """

    CommonServiceContext.comp_info["comp_id"] = comp.data.comp_id
    CommonServiceContext.comp_info["name"] = comp.data.name
    CommonServiceContext.comp_info["version"] = str(comp.data.version)

    from ...core.messaging import Channel
    from ...api import (
        PingCommand,
        PingReply,
        ServerConnectedEvent,
        ComponentInformationEvent,
    )

    svc = comp.create_service("Common service", context_type=CommonServiceContext)

    @svc.message_handler(PingCommand)
    def ping_command(msg: PingCommand, ctx: CommonServiceContext) -> None:
        ctx.logger.debug("Received PING", scope="component", payload=msg.payload)

        PingReply.emit(ctx.message_emitter, msg)

    @svc.message_handler(PingReply)
    def ping_reply(msg: PingReply, ctx: CommonServiceContext) -> None:
        ctx.logger.debug("Received PING reply", scope="component", payload=msg.payload)

    @svc.message_handler(ServerConnectedEvent)
    def server_connected(msg: ServerConnectedEvent, ctx: CommonServiceContext) -> None:
        # Whenever a client connects to our server, automatically send the server's component information
        _emit_comp_info(msg.comp_id, ctx)

    @svc.message_handler(ComponentInformationEvent)
    def component_information(
        msg: ComponentInformationEvent, ctx: CommonServiceContext
    ) -> None:
        from ...core.messaging.meta import MessageMetaInformation

        # If this message is received through the client, we need to send our information in return
        if ctx.meta_information.entrypoint == MessageMetaInformation.Entrypoint.CLIENT:
            _emit_comp_info(msg.comp_id, ctx)

    def _emit_comp_info(comp_id: UnitID, ctx: CommonServiceContext) -> None:
        ComponentInformationEvent.emit(
            ctx.message_emitter,
            Channel.direct(comp_id),
            comp_id=ctx.comp_info["comp_id"],
            comp_name=ctx.comp_info["name"],
            comp_version=ctx.comp_info["version"],
        )

    return svc
