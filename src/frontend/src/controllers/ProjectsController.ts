import { ListProjectsCommand, ListProjectsCommandReply } from "@common/api/ProjectCommands";
import { type CommandComposerExtender } from "@common/controllers/Controller";

import { BaseController } from "@/controllers/BaseController";

/**
 * Controller for projects.
 */
export class ProjectsController extends BaseController {
    /**
     * Requests the entire projects list of the current user.
     *
     * @param extender - An optional callback to extend the used composer.
     */
    public listProjects(extender: CommandComposerExtender<ListProjectsCommand> | null = null): void {
        const composer = this.messageBuilder.buildCommand(ListProjectsCommand).done((cmd: ListProjectsCommandReply, success: boolean, msg: string) => {
            console.log("Projects reply:");
            console.log(cmd.projects);
        });

        this.emitMessage(composer, extender);
    }
}
