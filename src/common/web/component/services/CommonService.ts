import { ComponentInformationEvent } from "../../api/ComponentEvents";
import { PingCommand, PingReply } from "../../api/NetworkCommands";
import { Channel } from "../../core/messaging/Channel";
import { Service } from "../../service/Service";
import { ServiceContext } from "../../service/ServiceContext";
import { WebComponent } from "../WebComponent";

/**
 * Creates the common service that handles various basic messaging tasks.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function (comp: WebComponent): Service {
    return comp.createService("Common service", (svc: Service) => {
        svc.messageHandler(PingCommand, (msg: PingCommand, ctx: ServiceContext) => {
            ctx.logger.debug("Received PING", "component", { payload: msg.payload });
        });

        svc.messageHandler(PingReply, (msg: PingReply, ctx: ServiceContext) => {
            ctx.logger.debug("Received PING reply", "component", { payload: msg.payload });
        });

        svc.messageHandler(ComponentInformationEvent, (msg: ComponentInformationEvent, ctx: ServiceContext) => {
            // This message is always received from the server side; we need to send our information in return
            let data = WebComponent.instance.data;
            ComponentInformationEvent.build(
                ctx.messageBuilder,
                data.compID,
                data.name,
                data.version.toString()
            ).emit(Channel.direct(msg.comp_id));
        });
    });
}
