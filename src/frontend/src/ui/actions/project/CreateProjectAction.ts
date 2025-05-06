import { CreateProjectCommand } from "@common/api/project/ProjectCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { ProjectOptions } from "@common/data/entities/project/ProjectOptions";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { StatusNotifier } from "@common/ui/actions/notifiers/StatusNotifier";
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

        this._composer = CreateProjectCommand.build(this.messageBuilder, resourcesPath, title, description, options);
        return this._composer;
    }

    protected addDefaultNotifiers(title: string): void {
        this.addNotifier(
            ActionState.Executing,
            new StatusNotifier(OverlayNotificationType.Info, `Creating project ${title}...`, "material-icons-outlined mi-description", true)
        );
        this.addNotifier(
            ActionState.Done,
            new StatusNotifier(OverlayNotificationType.Success, `Project '${title}' has been created.`, "material-icons-outlined mi-description")
        );
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
