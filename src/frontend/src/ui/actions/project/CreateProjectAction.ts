import { CreateProjectCommand } from "@common/api/project/ProjectCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { ProjectOptions } from "@common/data/entities/project/ProjectOptions";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { type ExtendedDialogResult } from "@common/ui/dialogs/ExtendedDialog";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";
import { editProjectDialog, type EditProjectDialogData } from "@/ui/dialogs/project/edit/EditProjectDialog";

/**
 * Action to create a project.
 */
export class CreateProjectAction extends FrontendCommandAction<CreateProjectCommand, CommandComposer<CreateProjectCommand>> {
    /**
     * Shows the edit project dialog.
     */
    public showEditDialog(): ExtendedDialogResult<EditProjectDialogData> {
        return editProjectDialog(this._component, undefined);
    }

    public prepare(resourcesPath: string, title: string, description: string, options: ProjectOptions): CommandComposer<CreateProjectCommand> {
        super.prepareNotifiers(title);

        this._composer = CreateProjectCommand.build(this.messageBuilder, resourcesPath, title, description, options).timeout(this._regularTimeout);
        return this._composer;
    }

    protected addDefaultNotifiers(title: string): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(OverlayNotificationType.Info, "Creating project", `Project '${title}' is being created...`)
        );
        this.addNotifier(ActionState.Done, new OverlayNotifier(OverlayNotificationType.Success, "Creating project", `Project '${title}' has been created.`));
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(
                OverlayNotificationType.Error,
                "Error creating project",
                `An error occurred while creating project '${title}': ${ActionNotifier.MessagePlaceholder}.`,
                true
            )
        );
    }
}
