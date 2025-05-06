import { GetMetadataProfilesCommand } from "@common/api/metadata/MetadataCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to retrieve all connectors.
 */
export class GetMetadataProfilesAction extends FrontendCommandAction<GetMetadataProfilesCommand, CommandComposer<GetMetadataProfilesCommand>> {
    public prepare(): CommandComposer<GetMetadataProfilesCommand> {
        this.prepareNotifiers();

        this._composer = GetMetadataProfilesCommand.build(this.messageBuilder);
        return this._composer;
    }

    protected addDefaultNotifiers(): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(OverlayNotificationType.Info, "Fetching metadata profiles", "The available metadata profiles are being downloaded..."),
            true
        );
        this.addNotifier(
            ActionState.Done,
            new OverlayNotifier(OverlayNotificationType.Success, "Fetching metadata profiles", "All metadata profiles have been downloaded."),
            true
        );
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(
                OverlayNotificationType.Error,
                "Error fetching metadata profiles",
                `An error occurred while downloading the metadata profiles: ${ActionNotifier.MessagePlaceholder}.`,
                true
            )
        );
    }
}
