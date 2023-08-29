import { networkStore } from "@/stores/NetworkStore";
import { ClientConnectedEvent, ClientConnectionErrorEvent, ClientDisconnectedEvent } from "@common/api/NetworkEvents";
import type { WebComponent } from "@common/component/WebComponent";
import { MessageContext } from "@common/core/messaging/handlers/MessageContext";
import type { Service } from "@common/service/Service";

export default function (comp: WebComponent): Service {
    let nwStore = networkStore();

    return comp.createService("Network service", (svc: Service) => {
        svc.messageHandler(ClientConnectedEvent.Name, ClientConnectedEvent,
            (msg: ClientConnectedEvent, ctx: MessageContext) => {
                nwStore.connected = true;
            });

        svc.messageHandler(ClientDisconnectedEvent.Name, ClientDisconnectedEvent,
            (msg: ClientDisconnectedEvent, ctx: MessageContext) => {
                nwStore.connected = false;
            });

        svc.messageHandler(ClientConnectionErrorEvent.Name, ClientConnectionErrorEvent,
            (msg: ClientConnectionErrorEvent, ctx: MessageContext) => {
                nwStore.connected = false;
            });
    });
}
