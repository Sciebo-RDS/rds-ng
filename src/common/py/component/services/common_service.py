from .. import BackendComponent
from ...service import Service


def create_common_service(comp: BackendComponent) -> Service:
    from ...api import PingCommand, PingReply
    from ...core.messaging.handlers import MessageContext

    svc = comp.create_service("Common service")

    @svc.message_handler(PingCommand)
    def ping_command(msg: PingCommand, ctx: MessageContext) -> None:
        ctx.logger.debug("Received PING", scope="component", payload=msg.payload)

        PingReply.emit(ctx.message_emitter, msg)

    @svc.message_handler(PingReply)
    def ping_reply(msg: PingReply, ctx: MessageContext) -> None:
        ctx.logger.debug("Received PING reply", scope="component", payload=msg.payload)

    return svc
