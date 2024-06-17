import { CreateProjectReply, DeleteProjectReply, ListProjectsReply, UpdateProjectReply } from "@common/api/project/ProjectCommands";
import { ProjectLogbookEvent, ProjectsListEvent } from "@common/api/project/ProjectEvents";
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
    return comp.createService(
        "Projects service",
        (svc: Service) => {
            svc.messageHandler(ListProjectsReply, (msg: ListProjectsReply, ctx: FrontendServiceContext) => {
                if (msg.success) {
                    ctx.logger.debug("Retrieved projects list", "projects", { projects: JSON.stringify(msg.projects) });

                    ctx.projectsStore.resetPendingDeletions();
                    // @ts-ignore
                    ctx.projectsStore.projects = msg.projects;
                } else {
                    ctx.logger.error("Unable to retrieve the projects list", "projects", { reason: msg.message });
                }
            });

            svc.messageHandler(ProjectsListEvent, (msg: ProjectsListEvent, ctx: FrontendServiceContext) => {
                ctx.logger.debug("Projects list update received", "projects", { projects: JSON.stringify(msg.projects) });

                ctx.projectsStore.resetPendingDeletions();
                // @ts-ignore
                ctx.projectsStore.projects = msg.projects;
            });

            svc.messageHandler(ProjectLogbookEvent, (msg: ProjectLogbookEvent, ctx: FrontendServiceContext) => {
                ctx.logger.debug("Project logbook update received", "projects", { project: msg.project_id, logbook: JSON.stringify(msg.logbook) });

                const project = ctx.projectsStore.projects.find((project) => project.project_id == msg.project_id);
                if (project) {
                    Object.assign(project, { logbook: msg.logbook });
                } else {
                    ctx.logger.warning("Received project logbook for an invalid project", "projects", {
                        project: msg.project_id,
                        logbook: JSON.stringify(msg.logbook),
                    });
                }
            });

            svc.messageHandler(CreateProjectReply, (msg: CreateProjectReply, ctx: FrontendServiceContext) => {
                if (msg.success) {
                    ctx.logger.debug(`Created project ${msg.project_id}`, "projects");

                    // @ts-ignore
                    ctx.projectsStore.activeProject = msg.project_id;
                } else {
                    ctx.logger.error(`Unable to create project ${msg.project_id}`, "projects", { reason: msg.message });
                }
            });

            svc.messageHandler(UpdateProjectReply, (msg: UpdateProjectReply, ctx: FrontendServiceContext) => {
                if (msg.success) {
                    ctx.logger.debug(`Updated project ${msg.project_id}`, "projects");
                } else {
                    ctx.logger.error(`Unable to Update project ${msg.project_id}`, "projects", { reason: msg.message });
                }
            });

            svc.messageHandler(DeleteProjectReply, (msg: DeleteProjectReply, ctx: FrontendServiceContext) => {
                ctx.projectsStore.unmarkForDeletion(msg.project_id);

                if (msg.success) {
                    ctx.logger.debug(`Deleted project ${msg.project_id}`, "projects");
                } else {
                    ctx.logger.error(`Unable to delete project ${msg.project_id}`, "projects", { reason: msg.message });
                }
            });
        },
        FrontendServiceContext,
    );
}
