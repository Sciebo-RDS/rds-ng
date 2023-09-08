import { ClientConnectionErrorEvent } from "../api/NetworkEvents";
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
        svc.messageHandler(ClientConnectionErrorEvent, (msg: ClientConnectionErrorEvent, ctx: ServiceContext) => {
            console.log("IHÖIUHIUHUIHIUHIUHIUHIU")
            const view = new ConnectionErrorView();
            view.activate(msg.reason).then();
        });
    });
}
