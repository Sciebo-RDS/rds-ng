import { ActionState } from "@common/ui/actions/ActionBase";
import { MultiAction } from "@common/ui/actions/MultiAction";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifier } from "@common/ui/actions/notifiers/OverlayNotifier";
import { OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

import { FrontendComponent } from "@/component/FrontendComponent";
import { ListUserAuthorizationsAction } from "@/ui/actions/authorization/ListUserAuthorizationsAction";
import { ListConnectorsAction } from "@/ui/actions/connector/ListConnectorsAction";
import { GetMetadataProfilesAction } from "@/ui/actions/metadata/GetMetadataProfilesAction";
import { ListProjectgExportersAction } from "@/ui/actions/project/ListProjectgExportersAction";
import { ListProjectJobsAction } from "@/ui/actions/project/ListProjectJobsAction";
import { ListProjectsAction } from "@/ui/actions/project/ListProjectsAction";
import { GetUserSettingsAction } from "@/ui/actions/user/GetUserSettingsAction";

/**
 * Multi-action to fetch all data from the server.
 */
export class GetAllDataAction extends MultiAction {
    public prepare(comp: FrontendComponent): void {
        this.prepareNotifiers();

        const listConAction = new ListConnectorsAction(comp, true);
        const getProfilesAction = new GetMetadataProfilesAction(comp, true);
        const getUserSettingsAction = new GetUserSettingsAction(comp, true);
        const listAuthorizationsAction = new ListUserAuthorizationsAction(comp, true);
        const listProjectsAction = new ListProjectsAction(comp, true);
        const listJobsAction = new ListProjectJobsAction(comp, true);
        const listExportersAction = new ListProjectgExportersAction(comp, true);

        listConAction.prepare();
        getProfilesAction.prepare();
        getUserSettingsAction.prepare();
        listAuthorizationsAction.prepare();
        listProjectsAction.prepare();
        listJobsAction.prepare();
        listExportersAction.prepare();

        this.addActions([
            listConAction,
            getProfilesAction,
            getUserSettingsAction,
            listAuthorizationsAction,
            listProjectsAction,
            listJobsAction,
            listExportersAction
        ]);
    }

    protected addDefaultNotifiers(): void {
        this.addNotifier(ActionState.Executing, new OverlayNotifier(OverlayNotificationType.Info, "Fetching data", "The data are being downloaded..."), true);
        this.addNotifier(ActionState.Done, new OverlayNotifier(OverlayNotificationType.Success, "Fetching data", "All data have been downloaded."), true);
        this.addNotifier(
            ActionState.Failed,
            new OverlayNotifier(
                OverlayNotificationType.Error,
                "Error fetching data",
                `An error occurred while downloading the data: ${ActionNotifier.MessagePlaceholder}.`,
                true
            )
        );
    }
}
