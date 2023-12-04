import { UpdateProjectCommand, UpdateProjectScope } from "@common/api/ProjectCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { Project, type ProjectID } from "@common/data/entities/Project";
import { type ProjectFeature, type ProjectFeatureID } from "@common/data/entities/ProjectFeature";
import { ActionState } from "@common/ui/actions/Action";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { type ExtendedDialogResult } from "@common/ui/dialogs/ExtendedDialog";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { editProjectDialog, type EditProjectDialogData } from "@/ui/dialogs/EditProjectDialog";
import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to update a project.
 */
export class UpdateProjectAction extends FrontendCommandAction<UpdateProjectCommand, CommandComposer<UpdateProjectCommand>> {
    /**
     * Shows the edit project dialog.
     *
     * @param project - The project to edit.
     */
    public showEditDialog(project: Project): ExtendedDialogResult<EditProjectDialogData> {
        return editProjectDialog(this._component, project);
    }

    public prepare(projectID: ProjectID, scope: UpdateProjectScope, title: string, description: string,
                   features: Map<ProjectFeatureID, ProjectFeature> = new Map<ProjectFeatureID, ProjectFeature>(),
                   featuresSelection: ProjectFeatureID[] = []
    ): CommandComposer<UpdateProjectCommand> {
        this.addDefaultNotifiers(title);

        this._composer = UpdateProjectCommand.build(this.messageBuilder, projectID, scope, title, description, features, featuresSelection).timeout(this._regularTimeout);
        return this._composer;
    }

    private addDefaultNotifiers(title: string): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(OverlayNotificationType.Info, "Updating project", `Project '${title}' is being updated...`)
        );
        this.addNotifier(ActionState.Done, new OverlayNotifier(OverlayNotificationType.Success, "Updating project", `Project '${title}' has been updated.`));
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(
                OverlayNotificationType.Error,
                "Error updating project",
                `An error occurred while updating project '${title}': ${ActionNotifier.MessagePlaceholder}.`,
                true
            )
        );
    }
}
