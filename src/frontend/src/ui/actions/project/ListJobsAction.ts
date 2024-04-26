import { ListJobsCommand } from "@common/api/project/ProjectJobCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to retrieve all projects.
 */
export class ListJobsAction extends FrontendCommandAction<ListJobsCommand, CommandComposer<ListJobsCommand>> {
    public prepare(): CommandComposer<ListJobsCommand> {
        this.prepareNotifiers();

        this._composer = ListJobsCommand.build(this.messageBuilder).timeout(this._regularTimeout);
        return this._composer;
    }

    protected addDefaultNotifiers(): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(OverlayNotificationType.Info, "Fetching jobs", "Your project jobs are being downloaded..."),
        );
        this.addNotifier(ActionState.Done, new OverlayNotifier(OverlayNotificationType.Success, "Fetching jobs", "Your project jobs have been downloaded."));
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(
                OverlayNotificationType.Error,
                "Error fetching jobs",
                `An error occurred while downloading your project jobs: ${ActionNotifier.MessagePlaceholder}.`,
                true,
            ),
        );
    }
}
