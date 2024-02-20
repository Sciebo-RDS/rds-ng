import { UpdateProjectFeaturesCommand } from "@common/api/project/ProjectFeaturesCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { ProjectFeature } from "@common/data/entities/project/features/ProjectFeature";
import { Project } from "@common/data/entities/project/Project";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to update the features of a project.
 */
export class UpdateProjectFeaturesAction extends FrontendCommandAction<UpdateProjectFeaturesCommand, CommandComposer<UpdateProjectFeaturesCommand>> {
    public prepare(project: Project, updatedFeatures: ProjectFeature[]): CommandComposer<UpdateProjectFeaturesCommand> {
        this.prepareNotifiers(project.title);

        this._composer = UpdateProjectFeaturesCommand.build(this.messageBuilder, project.project_id, updatedFeatures).timeout(this._regularTimeout);
        return this._composer;
    }

    protected addDefaultNotifiers(title: string): void {
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
                `An error occurred while updating the features of project '${title}': ${ActionNotifier.MessagePlaceholder}.`,
                true
            )
        );
    }
}
