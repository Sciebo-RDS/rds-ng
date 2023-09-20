import { ComponentInformationEvent } from "../api/ComponentEvents";
import { WebComponent } from "../component/WebComponent";
import { Channel } from "../core/messaging/Channel";
import { ComponentState, componentStore } from "../data/stores/ComponentStore";
import { ConnectionState, networkStore } from "../data/stores/NetworkStore";
import { Service } from "./Service";
import { ServiceContext } from "./ServiceContext";

/**
 * Creates the component service that reacts to basic messages.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function (comp: WebComponent): Service {
    return comp.createService("Component service", (svc: Service) => {
        const nwStore = networkStore();
        const compStore = componentStore();

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

            // Our connection to the server is now ready to be used; save the remote info and change our internal state to 'Running'
            nwStore.serverInfo = msg.componentInformation();
            nwStore.serverChannel = Channel.direct(msg.comp_id);

            nwStore.connectionState = ConnectionState.Ready;
            compStore.componentState = ComponentState.Running;

            WebComponent.instance.mainView.navigateTo();
        });
    });
}
