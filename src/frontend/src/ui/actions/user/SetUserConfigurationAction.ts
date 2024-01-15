import { SetUserConfigurationCommand } from "@common/api/user/UserCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { UserConfiguration } from "@common/data/entities/user/UserConfiguration";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to create a project.
 */
export class SetUserConfigurationAction extends FrontendCommandAction<SetUserConfigurationCommand, CommandComposer<SetUserConfigurationCommand>> {
    public prepare(userConfig: UserConfiguration): CommandComposer<SetUserConfigurationCommand> {
        super.prepareNotifiers();

        this._composer = SetUserConfigurationCommand.build(this.messageBuilder, userConfig).timeout(this._regularTimeout);
        return this._composer;
    }

    protected addDefaultNotifiers(): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(OverlayNotificationType.Info, "Updating user configuration", "Updating your configuration...")
        );
        this.addNotifier(ActionState.Done, new OverlayNotifier(OverlayNotificationType.Success, "Updating user configuration", "Your configuration has been updated."));
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(
                OverlayNotificationType.Error,
                "Error updating user configuration",
                `An error occurred while updating your configuration: ${ActionNotifier.MessagePlaceholder}.`,
                true
            )
        );
    }
}
