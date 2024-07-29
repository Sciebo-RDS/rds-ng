import { ref } from "vue";

import { UserSettings } from "@common/data/entities/user/UserSettings";

import { FrontendComponent } from "@/component/FrontendComponent";
import { SetUserSettingsAction } from "@/ui/actions/user/SetUserSettingsAction";

const _updatingUserSettings = ref(false);

export function useUserTools(comp: FrontendComponent) {
    function editUserSettings(userSettings: UserSettings): void {
        const action = new SetUserSettingsAction(comp);
        action.showUserSettingsDialog(userSettings).then(() => {});
    }

    function saveUserSettings(userSettings: UserSettings): void {
        _updatingUserSettings.value = true;

        const action = new SetUserSettingsAction(comp);
        action.prepare(userSettings).done(() => {
            _updatingUserSettings.value = false;
        });
        action.execute();
    }

    return {
        editUserSettings,
        saveUserSettings,
        updatingUserSettings: _updatingUserSettings
    };
}
