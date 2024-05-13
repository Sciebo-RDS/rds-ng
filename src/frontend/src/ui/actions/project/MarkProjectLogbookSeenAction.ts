import { MarkProjectLogbookSeenCommand } from "@common/api/project/ProjectCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { Project } from "@common/data/entities/project/Project";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to mark a project logbook entry as seen.
 */
export class MarkProjectLogbookSeenAction extends FrontendCommandAction<MarkProjectLogbookSeenCommand, CommandComposer<MarkProjectLogbookSeenCommand>> {
    public prepare(project: Project, record: number): CommandComposer<MarkProjectLogbookSeenCommand> {
        this.prepareNotifiers(project.title);

        this._composer = MarkProjectLogbookSeenCommand.build(this.messageBuilder, project.project_id, record).timeout(this._regularTimeout);
        return this._composer;
    }

    protected addDefaultNotifiers(title: string): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(OverlayNotificationType.Info, "Updating project logbook", `Project logbook '${title}' is being updated...`),
        );
        this.addNotifier(
            ActionState.Done,
            new OverlayNotifier(OverlayNotificationType.Success, "Updating project logbook", `Project logbook '${title}' has been updated.`),
        );
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(
                OverlayNotificationType.Error,
                "Error updating project logbook",
                `An error occurred while updating project logbook '${title}': ${ActionNotifier.MessagePlaceholder}.`,
                true,
            ),
        );
    }
}
