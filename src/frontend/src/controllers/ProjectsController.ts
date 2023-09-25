import { ListProjectsCommand } from "@common/api/ProjectCommands";
import { type CommandComposerExtender } from "@common/controllers/Controller";
import logging from "@common/core/logging/Logging";

import { FrontendController } from "@/controllers/FrontendController";

/**
 * Controller for projects.
 */
export class ProjectsController extends FrontendController {
    /**
     * Requests the entire projects list of the current user.
     *
     * @param extender - An optional callback to extend the used composer.
     */
    public listProjects(extender: CommandComposerExtender<ListProjectsCommand> | null = null): void {
        logging.debug("Fetching projects list...", "projects");

        const composer = this.messageBuilder.buildCommand(ListProjectsCommand);

        this.emitMessage(composer, extender);
    }
}
