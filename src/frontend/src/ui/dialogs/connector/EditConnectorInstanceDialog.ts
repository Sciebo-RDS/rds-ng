import { defineAsyncComponent } from "vue";

import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { extendedDialog, type ExtendedDialogResult } from "@common/ui/dialogs/ExtendedDialog";

import { FrontendComponent } from "@/component/FrontendComponent";

/**
 * The data used by the ``editConnectorInstanceDialog`` dialog.
 */
export interface EditConnectorInstanceDialogData {
    name: string;
    description: string;
}

/**
 * Shows the edit dialog for a connector instance.
 *
 * @param comp - The global component.
 * @param instance - The connector instance to edit.
 */
export async function editConnectorInstanceDialog(
    comp: FrontendComponent,
    instance: ConnectorInstance | undefined
): ExtendedDialogResult<EditConnectorInstanceDialogData> {
    return extendedDialog<EditConnectorInstanceDialogData>(
        comp,
        defineAsyncComponent(
            () => import("@/ui/dialogs/connector/EditConnectorInstanceDialog.vue")
        ),
        {
            header: instance ? "Connection settings" : "New connection",
            modal: true,
            contentClass: "w-[20vw] w-full min-w-[40rem] !pt-4"
        },
        {
            name: instance?.name || "",
            description: instance?.description || ""
        },
        {
            hasAcceptButton: true,
            acceptLabel: instance ? "Save" : "Create",
            acceptIcon: "material-icons-outlined mi-done",

            hasRejectButton: true,
            rejectLabel: "Cancel",
            rejectIcon: "material-icons-outlined mi-clear"
        }
    );
}
