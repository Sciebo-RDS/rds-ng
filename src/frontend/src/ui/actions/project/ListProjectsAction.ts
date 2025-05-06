import { ListProjectsCommand } from "@common/api/project/ProjectCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to retrieve all projects.
 */
export class ListProjectsAction extends FrontendCommandAction<ListProjectsCommand, CommandComposer<ListProjectsCommand>> {
    public prepare(): CommandComposer<ListProjectsCommand> {
        this.prepareNotifiers();

        this._composer = ListProjectsCommand.build(this.messageBuilder);
        return this._composer;
    }

    protected addDefaultNotifiers(): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(OverlayNotificationType.Info, "Fetching projects", "Your projects are being downloaded..."),
            true,
        );
        this.addNotifier(
            ActionState.Done,
            new OverlayNotifier(OverlayNotificationType.Success, "Fetching projects", "Your projects have been downloaded."),
            true,
        );
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(
                OverlayNotificationType.Error,
                "Error fetching projects",
                `An error occurred while downloading your projects: ${ActionNotifier.MessagePlaceholder}.`,
                true,
            ),
        );
    }
}
