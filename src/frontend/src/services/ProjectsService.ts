import { ListProjectsCommandReply } from "@common/api/ProjectCommands";
import { WebComponent } from "@common/component/WebComponent";
import { Service } from "@common/services/Service";

import { FrontendServiceContext } from "@/services/FrontendServiceContext";

/**
 * Creates the projects service.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function (comp: WebComponent): Service {
    return comp.createService("Projects service", (svc: Service) => {
        svc.messageHandler(ListProjectsCommandReply, (msg: ListProjectsCommandReply, ctx: FrontendServiceContext) => {
            ctx.logger.debug("Retrieved projects list", "projects", { projects: JSON.stringify(msg.projects) });

            ctx.store.projects = msg.projects;
        });
    }, FrontendServiceContext);
}
