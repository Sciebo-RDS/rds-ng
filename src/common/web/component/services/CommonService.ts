import { ComponentInformationEvent } from "../../api/ComponentEvents";
import { PingCommand, PingReply } from "../../api/NetworkCommands";
import { Channel } from "../../core/messaging/Channel";
import { Service } from "../../service/Service";
import { ServiceContext } from "../../service/ServiceContext";
import { UnitID } from "../../utils/UnitID";
import { WebComponent } from "../WebComponent";

/**
 * Context type for the common service.
 */
class CommonServiceContext extends ServiceContext {
    public static compInfo = {
        compID: new UnitID("", ""),
        name: "",
        version: "",
    };
}

/**
 * Creates the common service that handles various basic messaging tasks.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function (comp: WebComponent): Service {
    CommonServiceContext.compInfo.compID = comp.data.compID;
    CommonServiceContext.compInfo.name = comp.data.name;
    CommonServiceContext.compInfo.version = String(comp.data.version);

    return comp.createService("Common service", (svc: Service) => {
        svc.messageHandler(PingCommand, (msg: PingCommand, ctx: CommonServiceContext) => {
            ctx.logger.debug("Received PING", "component", { payload: msg.payload });

            PingReply.emit(ctx.messageEmitter, msg);
        });

        svc.messageHandler(PingReply, (msg: PingReply, ctx: CommonServiceContext) => {
            ctx.logger.debug("Received PING reply", "component", { payload: msg.payload });
        });

        svc.messageHandler(ComponentInformationEvent, (msg: ComponentInformationEvent, ctx: CommonServiceContext) => {
            // This message is always received from the server side; we need to send our information in return
            ComponentInformationEvent.emit(
                ctx.messageEmitter,
                Channel.direct(msg.comp_id),
                CommonServiceContext.compInfo.compID,
                CommonServiceContext.compInfo.name,
                CommonServiceContext.compInfo.version
            );
        });
    }, CommonServiceContext);
}
