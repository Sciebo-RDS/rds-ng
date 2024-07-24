import { SetUserSettingsCommand } from "@common/api/user/UserCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { UserSettings } from "@common/data/entities/user/UserSettings";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { type ExtendedDialogResult } from "@common/ui/dialogs/ExtendedDialog";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";
import { userSettingsDialog } from "@/ui/dialogs/user/settings/UserSettingsDialog";
import { type UserSettingsDialogData } from "@/ui/dialogs/user/settings/UserSettingsDialog";

/**
 * Action to create a project.
 */
export class EditUserSettingsAction extends FrontendCommandAction<SetUserSettingsCommand, CommandComposer<SetUserSettingsCommand>> {
    /**
     * Shows the user settings dialog.
     */
    public showUserSettingsDialog(userSettings: UserSettings): ExtendedDialogResult<UserSettingsDialogData> {
        return userSettingsDialog(this._component, userSettings);
    }

    public prepare(userSettings: UserSettings): CommandComposer<SetUserSettingsCommand> {
        super.prepareNotifiers();

        this._composer = SetUserSettingsCommand.build(this.messageBuilder, userSettings);
        return this._composer;
    }

    protected addDefaultNotifiers(): void {
        this.addNotifier(ActionState.Executing, new OverlayNotifier(OverlayNotificationType.Info, "Updating user settings", "Updating your settings..."), true);
        this.addNotifier(ActionState.Done, new OverlayNotifier(OverlayNotificationType.Success, "Updating user settings", "Your settings have been updated."));
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(
                OverlayNotificationType.Error,
                "Error updating user settings",
                `An error occurred while updating your settings: ${ActionNotifier.MessagePlaceholder}.`,
                true,
            ),
        );
    }
}
