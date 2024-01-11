import { ListConnectorsReply } from "@common/api/connector/ConnectorCommands";
import { ConnectorsListEvent } from "@common/api/connector/ConnectorEvents";
import { WebComponent } from "@common/component/WebComponent";
import { Service } from "@common/services/Service";

import { FrontendServiceContext } from "@/services/FrontendServiceContext";

/**
 * Creates the connectors service.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function(comp: WebComponent): Service {
    return comp.createService(
        "Connectors service",
        (svc: Service) => {
            svc.messageHandler(ListConnectorsReply, (msg: ListConnectorsReply, ctx: FrontendServiceContext) => {
                if (msg.success) {
                    ctx.logger.debug("Retrieved connectors list", "connectors", { connectors: JSON.stringify(msg.connectors) });

                    // @ts-ignore
                    ctx.connectorsStore.connectors = msg.connectors;
                } else {
                    ctx.logger.error("Unable to retrieve the connectors list", "connectors", { reason: msg.message });
                }
            });

            svc.messageHandler(ConnectorsListEvent, (msg: ConnectorsListEvent, ctx: FrontendServiceContext) => {
                ctx.logger.debug("Connectors list update received", "connectors", { connectors: JSON.stringify(msg.connectors) });

                // @ts-ignore
                ctx.connectorsStore.connectors = msg.connectors;
            });
        },
        FrontendServiceContext
    );
}
