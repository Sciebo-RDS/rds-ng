import { ListProjectExportersCommand } from "@common/api/project/ProjectExportersCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to retrieve all projects.
 */
export class ListProjectgExportersAction extends FrontendCommandAction<ListProjectExportersCommand, CommandComposer<ListProjectExportersCommand>> {
    public prepare(): CommandComposer<ListProjectExportersCommand> {
        this.prepareNotifiers();

        this._composer = ListProjectExportersCommand.build(this.messageBuilder);
        return this._composer;
    }

    protected addDefaultNotifiers(): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(OverlayNotificationType.Info, "Fetching exporters", "The available exporters are being downloaded..."),
            true
        );
        this.addNotifier(
            ActionState.Done,
            new OverlayNotifier(OverlayNotificationType.Success, "Fetching exporters", "All exporters have been downloaded."),
            true
        );
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(
                OverlayNotificationType.Error,
                "Error fetching exporters",
                `An error occurred while downloading the exporters: ${ActionNotifier.MessagePlaceholder}.`,
                true
            )
        );
    }
}
