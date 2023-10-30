import { DeleteProjectReply, ListProjectsReply } from "@common/api/ProjectCommands";
import { WebComponent } from "@common/component/WebComponent";
import { Service } from "@common/services/Service";

import { ProjectsServiceContext } from "@/services/ProjectsServiceContext";

/**
 * Creates the projects service.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function (comp: WebComponent): Service {
    return comp.createService("Projects service", (svc: Service) => {
        svc.messageHandler(ListProjectsReply, (msg: ListProjectsReply, ctx: ProjectsServiceContext) => {
            if (msg.success) {
                ctx.logger.debug("Retrieved projects list", "projects", { projects: JSON.stringify(msg.projects) });

                ctx.store.projects = msg.projects;
            } else {
                ctx.logger.error("Unable to retrieve the projects list", "projects", { reason: msg.message });
            }
        });

        svc.messageHandler(DeleteProjectReply, (msg: DeleteProjectReply, ctx: ProjectsServiceContext) => {
            if (msg.success) {
                ctx.logger.debug(`Deleted project ${msg.project_id}`, "projects", { projects: JSON.stringify(msg.projects) });
            } else {
                ctx.logger.error(`Unable to delete project ${msg.project_id}`, "projects", { reason: msg.message });
            }
        });
    }, ProjectsServiceContext);
}
