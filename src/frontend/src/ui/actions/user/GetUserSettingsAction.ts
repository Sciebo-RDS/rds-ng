import { GetUserSettingsCommand } from "@common/api/user/UserCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to retrieve all connectors.
 */
export class GetUserSettingsAction extends FrontendCommandAction<GetUserSettingsCommand, CommandComposer<GetUserSettingsCommand>> {
    public prepare(): CommandComposer<GetUserSettingsCommand> {
        this.prepareNotifiers();

        this._composer = GetUserSettingsCommand.build(this.messageBuilder).timeout(this._regularTimeout);
        return this._composer;
    }

    protected addDefaultNotifiers(): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(OverlayNotificationType.Info, "Fetching user settings", "Your settings are being downloaded...")
        );
        this.addNotifier(
            ActionState.Done,
            new OverlayNotifier(OverlayNotificationType.Success, "Fetching user settings", "Your settings have been downloaded.")
        );
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(OverlayNotificationType.Error, "Error fetching user settings", `An error occurred while downloading your settings: ${ActionNotifier.MessagePlaceholder}.`, true)
        );
    }
}
