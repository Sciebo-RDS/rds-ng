import { ListUserAuthorizationsCommand } from "@common/api/user/UserCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to retrieve all user authorizations.
 */
export class ListUserAuthorizationsAction extends FrontendCommandAction<ListUserAuthorizationsCommand, CommandComposer<ListUserAuthorizationsCommand>> {
    public prepare(): CommandComposer<ListUserAuthorizationsCommand> {
        this.prepareNotifiers();

        this._composer = ListUserAuthorizationsCommand.build(this.messageBuilder);
        return this._composer;
    }

    protected addDefaultNotifiers(): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(OverlayNotificationType.Info, "Fetching user authorizations", "The granted user authorizations are being downloaded..."),
        );
        this.addNotifier(
            ActionState.Done,
            new OverlayNotifier(OverlayNotificationType.Success, "Fetching user authorizations", "All user authorizations have been downloaded."),
        );
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(
                OverlayNotificationType.Error,
                "Error fetching user authorizations",
                `An error occurred while downloading the user authorizations: ${ActionNotifier.MessagePlaceholder}.`,
                true,
            ),
        );
    }
}
