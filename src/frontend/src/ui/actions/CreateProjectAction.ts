import { CreateProjectCommand } from "@common/api/ProjectCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { Project } from "@common/data/entities/Project";
import { ActionState } from "@common/ui/actions/Action";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { type ConfirmDialogResult } from "@common/ui/dialogs/ConfirmDialog";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { editProjectDialog } from "@/ui/dialogs/EditProjectDialog";
import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to create a project.
 */
export class CreateProjectAction extends FrontendCommandAction<CreateProjectCommand, CommandComposer<CreateProjectCommand>> {
    /**
     * Shows the edit project dialog.
     *
     * @param project - The project to edit.
     */
    public showEditDialog(project: Project): ConfirmDialogResult {
        return editProjectDialog(this._component, project);
    }

    public prepare(title: string, description: string): CommandComposer<CreateProjectCommand> {
        this.addDefaultNotifiers(title);

        this._composer = this.messageBuilder.buildCommand(CreateProjectCommand, { title: title, description: description }).timeout(this._regularTimeout);
        return this._composer;
    }

    private addDefaultNotifiers(title: string): void {
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
