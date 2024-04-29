import { ListProjectJobsReply } from "@common/api/project/ProjectJobCommands";
import { ProjectJobsListEvent } from "@common/api/project/ProjectJobEvents";
import { WebComponent } from "@common/component/WebComponent";
import { Service } from "@common/services/Service";

import { FrontendServiceContext } from "@/services/FrontendServiceContext";

/**
 * Creates the project jobs service.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function (comp: WebComponent): Service {
    return comp.createService(
        "Project jobs service",
        (svc: Service) => {
            svc.messageHandler(ListProjectJobsReply, (msg: ListProjectJobsReply, ctx: FrontendServiceContext) => {
                if (msg.success) {
                    ctx.logger.debug("Retrieved jobs list", "jobs", { jobs: JSON.stringify(msg.jobs) });

                    // @ts-ignore
                    ctx.projectJobsStore.jobs = msg.jobs;
                } else {
                    ctx.logger.error("Unable to retrieve the jobs list", "jobs", { reason: msg.message });
                }
            });

            svc.messageHandler(ProjectJobsListEvent, (msg: ProjectJobsListEvent, ctx: FrontendServiceContext) => {
                ctx.logger.debug("Jobs list update received", "jobs", { jobs: JSON.stringify(msg.jobs) });

                // @ts-ignore
                ctx.projectJobsStore.jobs = msg.jobs;
            });
        },
        FrontendServiceContext,
    );
}
