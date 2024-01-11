import { DeleteProjectCommand } from "@common/api/project/ProjectCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { Project } from "@common/data/entities/Project";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { type ConfirmDialogResult } from "@common/ui/dialogs/ConfirmDialog";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { projectsStore } from "@/data/stores/ProjectsStore";
import { confirmDeleteProjectDialog } from "@/ui/dialogs/ConfirmDeleteProjectDialog";
import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to delete a project.
 */
export class DeleteProjectAction extends FrontendCommandAction<DeleteProjectCommand, CommandComposer<DeleteProjectCommand>> {
    /**
     * Shows a confirmation dialog.
     *
     * @param project - The project to delete.
     */
    public showConfirmation(project: Project): ConfirmDialogResult {
        return confirmDeleteProjectDialog(this._component, project);
    }

    public prepare(project: Project): CommandComposer<DeleteProjectCommand> {
        this.markProjectForDeletion(project);

        this.prepareNotifiers(project);

        this._composer = DeleteProjectCommand.build(this.messageBuilder, project.project_id).timeout(this._regularTimeout);
        return this._composer;
    }

    private markProjectForDeletion(project: Project): void {
        const projStore = projectsStore();
        projStore.markForDeletion(project.project_id);
    }

    protected addDefaultNotifiers(project: Project): void {
        this.addNotifier(
            ActionState.Done,
            new OverlayNotifier(OverlayNotificationType.Success, "Delete project", `Project '${project.title}' (ID: ${project.project_id}) has been deleted.`)
        );
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(OverlayNotificationType.Error, "Error deleting project", `An error occurred while deleting project '${project.title}' (ID: ${project.project_id}): ${ActionNotifier.MessagePlaceholder}.`, true)
        );
    }
}
