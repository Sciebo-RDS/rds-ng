import { PingCommand, PingReply } from "../api/NetworkCommands";
import { ClientConnectedEvent, ClientConnectionErrorEvent, ClientDisconnectedEvent } from "../api/NetworkEvents";
import { WebComponent } from "../component/WebComponent";
import { ConnectionState, networkStore } from "../stores/NetworkStore";
import { Service } from "./Service";
import { ServiceContext } from "./ServiceContext";

/**
 * Creates the network service that reacts to general networking-related messages.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function (comp: WebComponent): Service {
    return comp.createService("Network service", (svc: Service) => {
        const nwStore = networkStore();

        svc.messageHandler(PingCommand, (msg: PingCommand, ctx: ServiceContext) => {
            ctx.logger.debug("Received PING", "component", { payload: msg.payload });

            PingReply.build(ctx.messageBuilder, msg).emit();
        });

        svc.messageHandler(PingReply, (msg: PingReply, ctx: ServiceContext) => {
            ctx.logger.debug("Received PING reply", "component", { payload: msg.payload });
        });

        svc.messageHandler(ClientConnectedEvent, (msg: ClientConnectedEvent, ctx: ServiceContext) => {
            // This event might be received _after_ the ComponentInformationEvent, so only elevated to 'connected' if we're not 'ready' yet
            if (nwStore.connectionState < ConnectionState.Ready) {
                nwStore.connectionState = ConnectionState.Connected;
            }
        });

        svc.messageHandler(ClientDisconnectedEvent, (msg: ClientDisconnectedEvent, ctx: ServiceContext) => {
            nwStore.reset();
        });

        svc.messageHandler(ClientConnectionErrorEvent, (msg: ClientConnectionErrorEvent, ctx: ServiceContext) => {
            nwStore.reset();
        });
    });
}
