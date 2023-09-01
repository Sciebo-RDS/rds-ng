import { ComponentInformationEvent } from "../api/ComponentEvents";
import { WebComponent } from "../component/WebComponent";
import { Channel } from "../core/messaging/Channel";
import { Service } from "./Service";
import { ServiceContext } from "./ServiceContext";

/**
 * Creates the common service that reacts to basic messages.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function (comp: WebComponent): Service {
    return comp.createService("Common service", (svc: Service) => {
        svc.messageHandler(ComponentInformationEvent, (msg: ComponentInformationEvent, ctx: ServiceContext) => {
            // This message is always received from the server side; we need to send our information in return
            let data = WebComponent.instance.data;
            ComponentInformationEvent.build(
                ctx.messageBuilder,
                data.compID,
                data.name,
                data.version.toString(),
                msg
            ).emit(Channel.direct(msg.comp_id));
        });
    });
}
