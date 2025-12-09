import { defineAsyncComponent } from "vue";

import { WebComponent } from "../../../component/WebComponent";
import { type BearerStrategyConfiguration } from "../../../integration/authorization/strategies/bearer/BearerTypes";
import { extendedDialog, type ExtendedDialogResult } from "../ExtendedDialog";

/**
 * The data used by the ``bearerCredentialsDialog`` dialog.
 */
export interface BearerTokenDialogData {
    bearerToken: string;

    config: BearerStrategyConfiguration;
}

/**
 * Shows the edit dialog for entering a bearer token.
 *
 * @param comp - The global component.
 * @param config - A bearer strategy configuration.
 */
export async function bearerTokenDialog(comp: WebComponent, config: BearerStrategyConfiguration): ExtendedDialogResult<BearerTokenDialogData> {
    return extendedDialog<BearerTokenDialogData>(
        comp,
        defineAsyncComponent(() => import("./BearerTokenDialog.vue")),
        {
            header: "Access token",
            modal: true,
            contentClass: "max-w-[20vw] w-[20vw] w-full min-w-[40rem]"
        },
        {
            bearerToken: "",
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
