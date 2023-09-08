import { DisconnectedView } from "@common/ui/views/landing/DisconnectedView";
import { ClientConnectionErrorEvent, ClientDisconnectedEvent } from "../api/NetworkEvents";
import { WebComponent } from "../component/WebComponent";
import { ConnectionErrorView } from "../ui/views/landing/ConnectionErrorView";
import { Service } from "./Service";
import { ServiceContext } from "./ServiceContext";

/**
 * Creates the web service that reacts to fundamental web ongoings.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function (comp: WebComponent): Service {
    return comp.createService("Web service", (svc: Service) => {
        svc.messageHandler(ClientDisconnectedEvent, (msg: ClientDisconnectedEvent, ctx: ServiceContext) => {
            // Navigate the user to the disconnected view
            const view = new DisconnectedView();
            view.activate().then();
        });

        svc.messageHandler(ClientConnectionErrorEvent, (msg: ClientConnectionErrorEvent, ctx: ServiceContext) => {
            // Navigate the user to the connection error view
            const view = new ConnectionErrorView();
            view.activate(msg.reason).then();
        });
    });
}
