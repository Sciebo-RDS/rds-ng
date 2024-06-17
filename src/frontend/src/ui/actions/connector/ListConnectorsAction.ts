import { ListConnectorsCommand } from "@common/api/connector/ConnectorCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to retrieve all connectors.
 */
export class ListConnectorsAction extends FrontendCommandAction<ListConnectorsCommand, CommandComposer<ListConnectorsCommand>> {
    public prepare(): CommandComposer<ListConnectorsCommand> {
        this.prepareNotifiers();

        this._composer = ListConnectorsCommand.build(this.messageBuilder);
        return this._composer;
    }

    protected addDefaultNotifiers(): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(OverlayNotificationType.Info, "Fetching connectors", "The available connectors are being downloaded..."),
        );
        this.addNotifier(ActionState.Done, new OverlayNotifier(OverlayNotificationType.Success, "Fetching connectors", "All connectors have been downloaded."));
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(
                OverlayNotificationType.Error,
                "Error fetching connectors",
                `An error occurred while downloading the connectors: ${ActionNotifier.MessagePlaceholder}.`,
                true,
            ),
        );
    }
}
