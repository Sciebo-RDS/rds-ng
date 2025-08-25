import { ref } from "vue";

import { UserSettings } from "@common/data/entities/user/UserSettings";

import { FrontendComponent } from "@/component/FrontendComponent";
import { GetUserSettingsAction } from "@/ui/actions/user/GetUserSettingsAction.ts";
import { SetUserSettingsAction } from "@/ui/actions/user/SetUserSettingsAction";
import { UserSettingsPage } from "@/ui/dialogs/user/settings/UserSettingsDialog.ts";

const _updatingUserSettings = ref(false);

export function useUserTools(comp: FrontendComponent) {
    function editUserSettings(userSettings: UserSettings, activePage: UserSettingsPage = UserSettingsPage.Connections): void {
        const action = new SetUserSettingsAction(comp);
        action.showUserSettingsDialog(userSettings, activePage).then(() => {});
    }

    function saveUserSettings(userSettings: UserSettings, fetchSettings: boolean = true): Promise<void> {
        _updatingUserSettings.value = true;

        return new Promise<void>((resolve, reject) => {
            const action = new SetUserSettingsAction(comp);
            action
                .prepare(userSettings)
                .done(() => {
                    if (fetchSettings) {
                        const getUserSettingsAction = new GetUserSettingsAction(comp, true);
                        getUserSettingsAction.prepare().done(() => {
                            _updatingUserSettings.value = false;
                            resolve();
                        });
                        getUserSettingsAction.execute();
                    } else {
                        _updatingUserSettings.value = false;
                        resolve();
                    }
                })
                .failed((err) => {
                    reject(err);
                });
            action.execute();
        });
    }

    function copyUserSettings(source: UserSettings, target: UserSettings): void {
        // @ts-ignore
        target.connector_instances = source.connector_instances;
    }

    return {
        editUserSettings,
        saveUserSettings,
        copyUserSettings,
        userSettingsUpdating: _updatingUserSettings
    };
}
