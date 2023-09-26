import { FrontendComponent } from "@/component/FrontendComponent";
import { ListProjectsCommand } from "@common/api/ProjectCommands";
import logging from "@common/core/logging/Logging";
import { CommandAction, type CommandActionCallback } from "@common/ui/actions/CommandAction";

/**
 * Action to retrieve all projects.
 */
export class ListProjectsAction extends CommandAction<ListProjectsCommand> {
    public constructor(comp: FrontendComponent) {
        super(comp.frontendService);
    }

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
