import { ListProjectsCommand } from "@common/api/ProjectCommands";
import logging from "@common/core/logging/Logging";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { type CommandActionCallback } from "@common/ui/actions/Action";

import { FrontendAction } from "@/ui/actions/FrontendAction";

/**
 * Action to retrieve all projects.
 */
export class ListProjectsAction extends FrontendAction<ListProjectsCommand, CommandComposer<ListProjectsCommand>> {
    /**
     * Requests the entire projects list of the current user.
     *
     * @param callback - An optional callback to extend the used message composer.
     */
    public execute(callback: CommandActionCallback<ListProjectsCommand> | null = null): void {
        logging.debug("Fetching projects list...", "projects");

        const composer = this.messageBuilder.buildCommand(ListProjectsCommand);
        this.executeAction(composer, callback);
    }
}
