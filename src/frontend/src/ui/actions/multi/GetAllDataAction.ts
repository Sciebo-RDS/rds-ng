import { FrontendComponent } from "@/component/FrontendComponent";
import { ListConnectorsAction } from "@/ui/actions/connector/ListConnectorsAction";
import { ListJobsAction } from "@/ui/actions/project/ListJobsAction";
import { ListProjectsAction } from "@/ui/actions/project/ListProjectsAction";
import { GetUserSettingsAction } from "@/ui/actions/user/GetUserSettingsAction";
import { ActionState } from "@common/ui/actions/ActionBase";
import { MultiAction } from "@common/ui/actions/MultiAction";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

/**
 * Multi-action to fetch all data from the server.
 */
export class GetAllDataAction extends MultiAction {
    public prepare(comp: FrontendComponent): void {
        this.prepareNotifiers();

        const listConAction = new ListConnectorsAction(comp, true);
        const getUserSettingsAction = new GetUserSettingsAction(comp, true);
        const listProjectsAction = new ListProjectsAction(comp, true);
        const listJobsAction = new ListJobsAction(comp, true);

        listConAction.prepare();
        getUserSettingsAction.prepare();
        listProjectsAction.prepare();
        listJobsAction.prepare();

        this.addActions([listConAction, getUserSettingsAction, listProjectsAction, listJobsAction]);
    }

    protected addDefaultNotifiers(): void {
        this.addNotifier(ActionState.Executing, new OverlayNotifier(OverlayNotificationType.Info, "Fetching data", "The data are being downloaded..."));
        this.addNotifier(ActionState.Done, new OverlayNotifier(OverlayNotificationType.Success, "Fetching data", "All data have been downloaded."));
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(
                OverlayNotificationType.Error,
                "Error fetching data",
                `An error occurred while downloading the data: ${ActionNotifier.MessagePlaceholder}.`,
                true,
            ),
        );
    }
}
