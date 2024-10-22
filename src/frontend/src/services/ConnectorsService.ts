import { ListConnectorsReply } from "@common/api/connector/ConnectorCommands";
import { ConnectorsListEvent } from "@common/api/connector/ConnectorEvents";
import { Connector } from "@common/data/entities/connector/Connector";
import { useColorsStore } from "@common/data/stores/ColorsStore";
import { Service } from "@common/services/Service";
import { deepClone, shortenDataStrings } from "@common/utils/ObjectUtils";

import { FrontendComponent } from "@/component/FrontendComponent";
import { FrontendServiceContext } from "@/services/FrontendServiceContext";

/**
 * Creates the connectors service.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function (comp: FrontendComponent): Service {
    function printableConnector(connector: Connector): string {
        let obj = deepClone<Connector>(connector);
        return JSON.stringify(shortenDataStrings(obj));
    }

    return comp.createService(
        "Connectors service",
        (svc: Service) => {
            svc.messageHandler(ListConnectorsReply, (msg: ListConnectorsReply, ctx: FrontendServiceContext) => {
                if (msg.success) {
                    const colorsStore = useColorsStore();

                    ctx.logger.debug("Retrieved connectors list", "connectors", { connectors: msg.connectors.map(printableConnector) });

                    // @ts-ignore
                    ctx.connectorsStore.connectors = msg.connectors;

                    colorsStore.populateFromConnectorsList(msg.connectors);
                } else {
                    ctx.logger.error("Unable to retrieve the connectors list", "connectors", { reason: msg.message });
                }
            });

            svc.messageHandler(ConnectorsListEvent, (msg: ConnectorsListEvent, ctx: FrontendServiceContext) => {
                ctx.logger.debug("Connectors list update received", "connectors", { connectors: msg.connectors.map(printableConnector) });

                // @ts-ignore
                ctx.connectorsStore.connectors = msg.connectors;

                assignConnectorProfileColors(msg.connectors);
            });
        },
        FrontendServiceContext
    );
}
