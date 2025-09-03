import { defineAsyncComponent } from "vue";

import { WebComponent } from "../../../component/WebComponent";
import { type BasicStrategyConfiguration } from "../../../integration/authorization/strategies/basic/BasicTypes";
import { extendedDialog, type ExtendedDialogResult } from "../ExtendedDialog";

/**
 * The data used by the ``basicCredentialsDialog`` dialog.
 */
export interface BasicCredentialsDialogData {
    userName: string;
    userPassword: string;

    config: BasicStrategyConfiguration;
}

/**
 * Shows the edit dialog for a connector instance.
 *
 * @param comp - The global component.
 * @param config - A basic strategy configuration.
 */
export async function basicCredentialsDialog(comp: WebComponent, config: BasicStrategyConfiguration): ExtendedDialogResult<BasicCredentialsDialogData> {
    return extendedDialog<BasicCredentialsDialogData>(
        comp,
        defineAsyncComponent(() => import("./BasicCredentialsDialog.vue")),
        {
            header: "Account credentials",
            modal: true,
            contentClass: "max-w-[20vw] w-[20vw] w-full min-w-[40rem]"
        },
        {
            userName: "",
            userPassword: "",
            config: config
        },
        {
            hasAcceptButton: true,
            acceptLabel: "Connect",
            acceptIcon: "material-icons-outlined mi-link",

            hasRejectButton: true,
            rejectLabel: "Cancel",
            rejectIcon: "material-icons-outlined mi-clear"
        },
        undefined,
        false
    );
}
