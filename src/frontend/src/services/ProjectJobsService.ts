import { ListProjectJobsReply } from "@common/api/project/ProjectJobCommands";
import { ProjectJobCompletionEvent, ProjectJobsListEvent } from "@common/api/project/ProjectJobEvents";
import { WebComponent } from "@common/component/WebComponent";
import { findConnectorByInstanceID, findConnectorInstanceByID } from "@common/data/entities/connector/ConnectorUtils";
import { findProjectByID } from "@common/data/entities/project/ProjectUtils";
import { Service } from "@common/services/Service";
import { OverlayNotifications } from "@common/ui/notifications/OverlayNotifications";

import { getConnectorCategory } from "@/data/entities/connector/ConnectorUtils";
import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useProjectsStore } from "@/data/stores/ProjectsStore";
import { useUserStore } from "@/data/stores/UserStore";
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

            svc.messageHandler(ProjectJobCompletionEvent, (msg: ProjectJobCompletionEvent, ctx: FrontendServiceContext) => {
                ctx.logger.debug("Job completed", "jobs", {
                    projectID: msg.project_id,
                    connectorInstance: msg.connector_instance,
                    success: msg.success,
                    message: msg.message,
                });

                const projStore = useProjectsStore();
                const userStore = useUserStore();
                const conStore = useConnectorsStore();

                const project = findProjectByID(projStore.projects, msg.project_id);
                const connector = findConnectorByInstanceID(conStore.connectors, userStore.userSettings.connector_instances, msg.connector_instance);
                const connectorInstance = findConnectorInstanceByID(userStore.userSettings.connector_instances, msg.connector_instance);
                const category = connector ? getConnectorCategory(connector) : undefined;

                const notifications = new OverlayNotifications(comp);
                if (msg.success) {
                    notifications.success(
                        "Job completed",
                        `${category?.verbNoun || "Execution"} of project '${project?.title || "(unknown project)"}' through connection ${connectorInstance?.name || "(unknown connection)"} has finished successfully.`,
                        true,
                    );
                } else {
                    notifications.error(
                        "Job failed",
                        `${category?.verbNoun || "Execution"} of project '${project?.title || "(unknown project)"}' through connection ${connectorInstance?.name || "(unknown connection)"} has failed: ${msg.message}`,
                        true,
                    );
                }
            });
        },
        FrontendServiceContext,
    );
}
