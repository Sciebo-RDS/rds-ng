import { UserSettings } from "@common/data/entities/user/UserSettings";

import { FrontendComponent } from "@/component/FrontendComponent";
import { EditUserSettingsAction } from "@/ui/actions/user/EditUserSettingsAction";

export function useUserTools(comp: FrontendComponent) {
    function editUserSettings(userSettings: UserSettings): void {
        const action = new EditUserSettingsAction(comp);
        action.showUserSettingsDialog(userSettings).then((data) => {
            action.prepare(data.userSettings);
            action.execute();
        });
    }

    return {
        editUserSettings,
    };
}
