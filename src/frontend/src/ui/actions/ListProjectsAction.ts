import { ListProjectsCommand } from "@common/api/ProjectCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to retrieve all projects.
 */
export class ListProjectsAction extends FrontendCommandAction<ListProjectsCommand, CommandComposer<ListProjectsCommand>> {
    public prepare(): CommandComposer<ListProjectsCommand> {
        this._composer = this.messageBuilder
            .buildCommand(ListProjectsCommand)
            .timeout(this._regularTimeout);
        return this._composer;
    }
}
