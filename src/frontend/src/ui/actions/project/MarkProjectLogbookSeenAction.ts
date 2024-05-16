import { MarkProjectLogbookSeenCommand } from "@common/api/project/ProjectCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { ProjectLogbookType } from "@common/data/entities/project/logbook/ProjectLogbookType";
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
    public prepare(logbookType: ProjectLogbookType, markAll: boolean, project?: Project, record?: number): CommandComposer<MarkProjectLogbookSeenCommand> {
        this.prepareNotifiers(project?.title);

        this._composer = MarkProjectLogbookSeenCommand.build(this.messageBuilder, logbookType, project?.project_id || 0, record || 0, markAll).timeout(
            this._regularTimeout,
        );
        return this._composer;
    }

    protected addDefaultNotifiers(title: string | undefined): void {
        if (title) {
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
        } else {
            this.addNotifier(
                ActionState.Executing,
                new OverlayNotifier(OverlayNotificationType.Info, "Updating project logbooks", "All project logbooks are being updated..."),
            );
            this.addNotifier(
                ActionState.Done,
                new OverlayNotifier(OverlayNotificationType.Success, "Updating project logbooks", "All project logbooks have been updated."),
            );
            this.addNotifier(
                ActionState.Failed,
                new OverlayNotifier(
                    OverlayNotificationType.Error,
                    "Error updating project logbooks",
                    "An error occurred while updating project logbooks: ${ActionNotifier.MessagePlaceholder}.",
                    true,
                ),
            );
        }
    }
}
