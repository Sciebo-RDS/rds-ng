import { ListProjectsCommand } from "@common/api/ProjectCommands";
import logging from "@common/core/logging/Logging";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";

import { FrontendAction } from "@/ui/actions/FrontendAction";

/**
 * Action to retrieve all projects.
 */
export class ListProjectsAction extends FrontendAction<ListProjectsCommand, CommandComposer<ListProjectsCommand>> {
    public prepare(): CommandComposer<ListProjectsCommand> {
        this._composer = this.messageBuilder.buildCommand(ListProjectsCommand);
        return this._composer;
    }

    protected preExecution(): void {
        logging.debug("Fetching projects list...", "projects");
    }
}
