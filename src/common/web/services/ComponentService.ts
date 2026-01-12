import { SemVer } from "semver";
import { ComponentInformationEvent } from "../api/component/ComponentEvents";
import { API_PROTOCOL_VERSION, checkProtocolCompatibility, ProtocolCompatibility } from "../api/Version";
import { WebComponent } from "../component/WebComponent";
import logging from "../core/logging/Logging";
import { Channel } from "../core/messaging/Channel";
import { ComponentState, useComponentStore } from "../data/stores/ComponentStore";
import { ConnectionState, useNetworkStore } from "../data/stores/NetworkStore";
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
        const nwStore = useNetworkStore();
        const compStore = useComponentStore();

        svc.messageHandler(ComponentInformationEvent, (msg: ComponentInformationEvent, ctx: ServiceContext) => {
            // Notify of mismatching API protocol versions, which might lead to errors in network communication
            const protocolCompat = checkProtocolCompatibility(new SemVer(msg.api_protocol));
            if (protocolCompat == ProtocolCompatibility.NotCompatible) {
                logging.error("API major version mismatch; the affected components will not work together properly", "network", {
                    component: msg.comp_id,
                    got: msg.api_protocol,
                    want: API_PROTOCOL_VERSION.toString()
                });
            } else if (protocolCompat == ProtocolCompatibility.MaybeCompatible) {
                logging.warning("API minor version mismatch; the affected components might not work together properly", "network", {
                    component: msg.comp_id,
                    got: msg.api_protocol,
                    want: API_PROTOCOL_VERSION.toString()
                });
            }

            // This message is always received from the server side; we need to send our information in return
            const data = WebComponent.instance.data;
            ComponentInformationEvent.build(ctx.messageBuilder, data.compID, data.name, data.version.toString(), msg).emit(Channel.direct(msg.comp_id));

            // Our connection to the server is now ready to be used; save the remote info and change our internal state to 'Running'
            nwStore.serverInfo = msg.componentInformation();
            nwStore.serverChannel = Channel.direct(msg.comp_id);

            nwStore.connectionState = ConnectionState.Ready;
            compStore.componentState = ComponentState.Running;
        });
    });
}
