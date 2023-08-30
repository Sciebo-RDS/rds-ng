import { PingCommand, PingReply } from "../../api/PingCommand";
import { MessageContext } from "../../core/messaging/handlers/MessageContext";
import { Service } from "../../service/Service";
import { WebComponent } from "../WebComponent";

export default function (comp: WebComponent): Service {
    return comp.createService("Common service", (svc: Service) => {
        svc.messageHandler(PingCommand, (msg: PingCommand, ctx: MessageContext) => {
            ctx.logger.debug("Received PING", "component", { payload: msg.payload });

            ctx.messageEmitter.emitReply(PingReply, msg);
        });

        svc.messageHandler(PingReply, (msg: PingReply, ctx: MessageContext) => {
            ctx.logger.debug("Received PING reply", "component", { payload: msg.payload });
        });
    });
}
