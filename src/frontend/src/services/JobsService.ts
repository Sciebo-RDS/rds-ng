import { ListJobsReply } from "@common/api/project/ProjectJobCommands";
import { JobsListEvent } from "@common/api/project/ProjectJobEvents";
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
        "Jobs service",
        (svc: Service) => {
            svc.messageHandler(ListJobsReply, (msg: ListJobsReply, ctx: FrontendServiceContext) => {
                if (msg.success) {
                    ctx.logger.debug("Retrieved jobs list", "jobs", { projects: JSON.stringify(msg.project_jobs) });

                    // @ts-ignore
                    ctx.jobsStore.jobs = msg.project_jobs;
                } else {
                    ctx.logger.error("Unable to retrieve the jobs list", "jobs", { reason: msg.message });
                }
            });

            svc.messageHandler(JobsListEvent, (msg: JobsListEvent, ctx: FrontendServiceContext) => {
                ctx.logger.debug("Jobs list update received", "jobs", { projects: JSON.stringify(msg.project_jobs) });

                // @ts-ignore
                ctx.jobsStore.jobs = msg.project_jobs;
            });
        },
        FrontendServiceContext,
    );
}
