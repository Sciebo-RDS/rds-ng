import { ListResourcesCommand } from "@common/api/resource/ResourceCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { ActionState } from "@common/ui/actions/ActionBase";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to retrieve all resources (i.e., files and folders).
 */
export class ListResourcesAction extends FrontendCommandAction<ListResourcesCommand, CommandComposer<ListResourcesCommand>> {
    public prepare(root: string = "", includeFolders: boolean = true, includeFiles: boolean = true, recursive: boolean = true): CommandComposer<ListResourcesCommand> {
        this.prepareNotifiers();

        this._composer = ListResourcesCommand.build(this.messageBuilder, root, includeFolders, includeFiles, recursive).timeout(this._regularTimeout);
        return this._composer;
    }

    protected addDefaultNotifiers(): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(OverlayNotificationType.Info, "Fetching resources", "The list of your resources is being downloaded...")
        );
        this.addNotifier(
            ActionState.Done,
            new OverlayNotifier(OverlayNotificationType.Success, "Fetching resources", "The list of your resources has been downloaded.")
        );
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(OverlayNotificationType.Error, "Error fetching resources", `An error occurred while downloading your resources list: ${ActionNotifier.MessagePlaceholder}.`, true)
        );
    }
}
