import { DeleteProjectCommand } from "@common/api/ProjectCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { Project } from "@common/data/entities/Project";
import { ActionState } from "@common/ui/actions/Action";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to delete a project.
 */
export class DeleteProjectAction extends FrontendCommandAction<DeleteProjectCommand, CommandComposer<DeleteProjectCommand>> {
    public prepare(project: Project): CommandComposer<DeleteProjectCommand> {
        this.addDefaultNotifiers(project);

        this._composer = this.messageBuilder
            .buildCommand(DeleteProjectCommand, { project_id: project.project_id })
            .timeout(this._regularTimeout);
        return this._composer;
    }

    private addDefaultNotifiers(project: Project): void {
        this.addNotifier(
            ActionState.Done,
            new OverlayNotifier(OverlayNotificationType.Success, "Delete project", `Project '${project.name}' (ID: ${project.project_id}) has been deleted.`)
        );
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(OverlayNotificationType.Error, "Error deleting project", `An error occurred while deleting project '${project.name}' (ID: ${project.project_id}): ${ActionNotifier.MessagePlaceholder}.`, true)
        );
    }
}
