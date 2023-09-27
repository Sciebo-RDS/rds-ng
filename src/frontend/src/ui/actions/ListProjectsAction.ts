import { ListProjectsCommand } from "@common/api/ProjectCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { CommandAction } from "@common/ui/actions/CommandAction";

/**
 * Action to retrieve all projects.
 */
export class ListProjectsAction extends CommandAction<ListProjectsCommand, CommandComposer<ListProjectsCommand>> {
    public prepare(): CommandComposer<ListProjectsCommand> {
        this._composer = this.messageBuilder.buildCommand(ListProjectsCommand);
        return this._composer;
    }
}
