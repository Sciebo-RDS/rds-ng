import { ClientConnectionErrorEvent, ClientDisconnectedEvent } from "../api/NetworkEvents";
import { WebComponent } from "../component/WebComponent";
import { ComponentState, componentStore } from "../stores/ComponentStore";
import { MainView } from "../ui/views/main/MainView";
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
        const compStore = componentStore();

        svc.messageHandler(ClientDisconnectedEvent, (msg: ClientDisconnectedEvent, ctx: ServiceContext) => {
            compStore.componentState = ComponentState.ConnectionLost;
            compStore.componentStateMessage = "Connection lost";

            const view = new MainView();
            view.activate().then();
        });

        svc.messageHandler(ClientConnectionErrorEvent, (msg: ClientConnectionErrorEvent, ctx: ServiceContext) => {
            compStore.componentState = ComponentState.ConnectionError;
            compStore.componentStateMessage = msg.reason;

            const view = new MainView();
            view.activate().then();
        });
    });
}
