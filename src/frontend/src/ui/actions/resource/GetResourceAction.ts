import { GetResourceCommand } from "@common/api/resource/ResourceCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { Resource } from "@common/data/entities/resource/Resource";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to retrieve a single resource.
 */
export class GetResourceAction extends FrontendCommandAction<GetResourceCommand, CommandComposer<GetResourceCommand>> {
    public prepare(resource: Resource): CommandComposer<GetResourceCommand> {
        this.prepareNotifiers(resource);

        this._composer = GetResourceCommand.build(this.messageBuilder, resource);
        return this._composer;
    }

    protected addDefaultNotifiers(resource: Resource): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(OverlayNotificationType.Info, "Fetching resource", `Resource ${resource.filename} is being downloaded...`),
            true,
        );
        this.addNotifier(
            ActionState.Done,
            new OverlayNotifier(OverlayNotificationType.Success, "Fetching resource", `Resource ${resource.filename} has been downloaded.`),
            true,
        );
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(
                OverlayNotificationType.Error,
                "Error downloading resource",
                `An error occurred while downloading resource ${resource.filename}: ${ActionNotifier.MessagePlaceholder}.`,
                true,
            ),
        );
    }
}
