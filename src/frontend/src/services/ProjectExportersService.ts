import { WebComponent } from "@common/component/WebComponent";
import { Service } from "@common/services/Service";

import { FrontendServiceContext } from "@/services/FrontendServiceContext";
import { ListProjectExportersReply } from "@common/api/project/ProjectExportersCommands";

/**
 * Creates the project exporters service.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function (comp: WebComponent): Service {
    return comp.createService(
        "Project exporters service",
        (svc: Service) => {
            svc.messageHandler(ListProjectExportersReply, (msg: ListProjectExportersReply, ctx: FrontendServiceContext) => {
                if (msg.success) {
                    ctx.logger.debug("Retrieved exporters list", "exporters", { exporters: JSON.stringify(msg.exporters) });

                    // @ts-ignore
                    ctx.projectExportersStore.exporters = msg.exporters;
                } else {
                    ctx.logger.error("Unable to retrieve the exporters list", "exporters", { reason: msg.message });
                }
            });
        },
        FrontendServiceContext
    );
}
