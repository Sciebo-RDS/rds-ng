import { publishProjectDialog } from "@/ui/dialogs/project/publish/PublishProjectDialog";
import { type PublishProjectDialogData } from "@/ui/dialogs/project/publish/PublishProjectDialog";
import { Command } from "@common/core/messaging/Command";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { Project } from "@common/data/entities/project/Project";
import { type ExtendedDialogResult } from "@common/ui/dialogs/ExtendedDialog";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to publish a project.
 */
export class PublishProjectAction extends FrontendCommandAction<Command, CommandComposer<Command>> {
    /**
     * Shows the publish project dialog.
     *
     * @param project - The project to publish.
     */
    public showPublishDialog(project: Project): ExtendedDialogResult<PublishProjectDialogData> {
        return publishProjectDialog(this._component, project);
    }

    public prepare(): CommandComposer<Command> {
        this.prepareNotifiers();

        // @ts-ignore
        return new CommandComposer<Command>();
    }

    protected addDefaultNotifiers(): void {
    }
}
