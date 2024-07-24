import { ListProjectJobsCommand } from "@common/api/project/ProjectJobCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to retrieve all projects.
 */
export class ListProjectJobsAction extends FrontendCommandAction<ListProjectJobsCommand, CommandComposer<ListProjectJobsCommand>> {
    public prepare(): CommandComposer<ListProjectJobsCommand> {
        this.prepareNotifiers();

        this._composer = ListProjectJobsCommand.build(this.messageBuilder);
        return this._composer;
    }

    protected addDefaultNotifiers(): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(OverlayNotificationType.Info, "Fetching jobs", "Your project jobs are being downloaded..."),
            true,
        );
        this.addNotifier(
            ActionState.Done,
            new OverlayNotifier(OverlayNotificationType.Success, "Fetching jobs", "Your project jobs have been downloaded."),
            true,
        );
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
