import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";
import { RevokeAuthorizationCommand } from "@common/api/authorization/AuthorizationCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

/**
 * Action to revoke an authorization.
 */
export class RevokeAuthorizationAction extends FrontendCommandAction<RevokeAuthorizationCommand, CommandComposer<RevokeAuthorizationCommand>> {
    public prepare(authID: string, title: string): CommandComposer<RevokeAuthorizationCommand> {
        this.prepareNotifiers(title);

        this._composer = RevokeAuthorizationCommand.build(this.messageBuilder, "", authID); // We pass an empty user ID, as this will be filled out be the server
        return this._composer;
    }

    protected addDefaultNotifiers(title: string): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(OverlayNotificationType.Info, "Revoking authorization", `The authorization for ${title} is being revoked...`),
        );
        this.addNotifier(
            ActionState.Done,
            new OverlayNotifier(OverlayNotificationType.Success, "Revoking authorization", `The authorization for ${title} has been revoked.`),
        );
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(
                OverlayNotificationType.Error,
                "Error revoking authorization",
                `An error occurred while revoking the authorization for ${title}: ${ActionNotifier.MessagePlaceholder}.`,
                true,
            ),
        );
    }
}
