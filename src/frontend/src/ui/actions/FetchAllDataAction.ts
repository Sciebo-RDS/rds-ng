import { FrontendComponent } from "@/component/FrontendComponent";
import { ListConnectorsAction } from "@/ui/actions/ListConnectorsAction";
import { ListProjectsAction } from "@/ui/actions/ListProjectsAction";
import { ActionState } from "@common/ui/actions/ActionBase";
import { MultiAction } from "@common/ui/actions/MultiAction";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

export class FetchAllDataAction extends MultiAction {
    public prepare(comp: FrontendComponent): void {
        this.prepareNotifiers();

        const listConAction = new ListConnectorsAction(comp);
        const listProjAction = new ListProjectsAction(comp);

        listConAction.suppressDefaultNotifiers = true;
        listConAction.prepare();
        listProjAction.suppressDefaultNotifiers = true;
        listProjAction.prepare();

        this.addActions([listConAction, listProjAction]);
    }

    protected addDefaultNotifiers(): void {
        this.addNotifier(
            ActionState.Executing,
            new OverlayNotifier(OverlayNotificationType.Info, "Fetching data", "The data are being downloaded...")
        );
        this.addNotifier(
            ActionState.Done,
            new OverlayNotifier(OverlayNotificationType.Success, "Fetching data", "All data have been downloaded.")
        );
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(OverlayNotificationType.Error, "Error fetching data", `An error occurred while downloading the data: ${ActionNotifier.MessagePlaceholder}.`, true)
        );
    }
}
