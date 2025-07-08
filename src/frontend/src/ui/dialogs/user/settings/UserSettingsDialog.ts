import { defineAsyncComponent } from "vue";

import { UserSettings } from "@common/data/entities/user/UserSettings";
import { extendedDialog, type ExtendedDialogResult } from "@common/ui/dialogs/ExtendedDialog";
import { deepClone } from "@common/utils/ObjectUtils";

import { FrontendComponent } from "@/component/FrontendComponent";

/**
 * The active page of the settings dialog.
 */
export const enum UserSettingsPage {
    Connections = 0,
    Support = 1,
    About = 2
}

/**
 * The data used by the ``UserSettingsDialog``.
 */
export interface UserSettingsDialogData {
    userSettings: UserSettings;

    activePage: UserSettingsPage;
}

/**
 * Shows the user settings dialog.
 *
 * @param comp - The global component.
 * @param userSettings - The current user settings.
 * @param activePage - The page to activate immediately.
 */
export async function userSettingsDialog(
    comp: FrontendComponent,
    userSettings: UserSettings,
    activePage: UserSettingsPage = UserSettingsPage.Connections
): ExtendedDialogResult<UserSettingsDialogData> {
    return extendedDialog<UserSettingsDialogData>(
        comp,
        defineAsyncComponent(() => import("@/ui/dialogs/user/settings/UserSettingsDialog.vue")),
        {
            header: "Settings",
            modal: true,
            dismissableMask: true,
            contentClass: "w-[75rem] h-[45rem]"
        },
        {
            userSettings: deepClone<UserSettings>(userSettings),
            activePage: activePage
        },
        {
            hasAcceptButton: true,
            acceptLabel: "Close",
            acceptOnClose: true
        }
    );
}
