import { defineAsyncComponent } from "vue";

import { UserSettings } from "@common/data/entities/user/UserSettings";
import { extendedDialog, type ExtendedDialogResult } from "@common/ui/dialogs/ExtendedDialog";
import { deepClone } from "@common/utils/ObjectUtils";

import { FrontendComponent } from "@/component/FrontendComponent";

/**
 * The data used by the ``UserSettingsDialog``.
 */
export interface UserSettingsDialogData {
    userSettings: UserSettings;
}

/**
 * Shows the user settings dialog.
 *
 * @param comp - The global component.
 * @param userSettings - The current user settings.
 */
export async function userSettingsDialog(comp: FrontendComponent, userSettings: UserSettings): ExtendedDialogResult<UserSettingsDialogData> {
    return extendedDialog<UserSettingsDialogData>(
        comp,
        defineAsyncComponent(() => import("@/ui/dialogs/user/settings/UserSettingsDialog.vue")),
        {
            header: "User settings",
            modal: true,
            dismissableMask: true,
            contentClass: "w-[70rem] h-[40rem]",
        },
        {
            userSettings: deepClone<UserSettings>(userSettings),
        },
        {
            hasAcceptButton: true,
            acceptLabel: "Close",
            acceptIcon: "material-icons-outlined mi-close",
            acceptOnClose: true,
        },
    );
}
