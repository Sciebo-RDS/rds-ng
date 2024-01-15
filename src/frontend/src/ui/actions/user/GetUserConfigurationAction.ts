import { GetUserConfigurationCommand } from "@common/api/user/UserCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to retrieve all connectors.
 */
export class GetUserConfigurationAction extends FrontendCommandAction<GetUserConfigurationCommand, CommandComposer<GetUserConfigurationCommand>> {
    public prepare(): CommandComposer<GetUserConfigurationCommand> {
        this.prepareNotifiers();

        this._composer = GetUserConfigurationCommand.build(this.messageBuilder).timeout(this._regularTimeout);
        return this._composer;
    }

    protected addDefaultNotifiers(): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(OverlayNotificationType.Info, "Fetching user configuration", "Your configuration is being downloaded...")
        );
        this.addNotifier(
            ActionState.Done,
            new OverlayNotifier(OverlayNotificationType.Success, "Fetching user configuration", "Your configuration has been downloaded.")
        );
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(OverlayNotificationType.Error, "Error fetching user configuration", `An error occurred while downloading your configuration: ${ActionNotifier.MessagePlaceholder}.`, true)
        );
    }
}
