import { ListProjectExportersReply } from "@common/api/project/ProjectExportersCommands";
import { Service } from "@common/services/Service";

import { FrontendComponent } from "@/component/FrontendComponent";
import { FrontendServiceContext } from "@/services/FrontendServiceContext";

/**
 * Creates the project exporters service.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function (comp: FrontendComponent): Service {
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
