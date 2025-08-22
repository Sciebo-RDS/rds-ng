import { defineAsyncComponent } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";

import { Connector } from "@common/data/entities/connector/Connector";
import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { connectorRequiresAuthorization } from "@common/data/entities/connector/ConnectorUtils.ts";
import { extendedDialog, type ExtendedDialogResult } from "@common/ui/dialogs/ExtendedDialog";

/**
 * The data used by the ``editConnectorInstanceDialog`` dialog.
 */
export interface EditConnectorInstanceDialogData {
    name: string;
    description: string;

    requiresAuth: boolean;
}

/**
 * Shows the edit dialog for a connector instance.
 *
 * @param comp - The global component.
 * @param instance - The connector instance to edit.
 * @param connector - The connector used by the instance.
 */
export async function editConnectorInstanceDialog(
    comp: FrontendComponent,
    instance?: ConnectorInstance,
    connector?: Connector
): ExtendedDialogResult<EditConnectorInstanceDialogData> {
    const isNewInstance = !instance;
    const requiresAuth = !!connector ? connectorRequiresAuthorization(connector) : false;

    return extendedDialog<EditConnectorInstanceDialogData>(
        comp,
        defineAsyncComponent(() => import("@/ui/dialogs/connector/instance/EditConnectorInstanceDialog.vue")),
        {
            header: (isNewInstance ? "New connection" : "Connection settings") + ` (${connector ? connector.name : "unknown connector"})`,
            modal: true,
            contentClass: "max-w-[20vw] w-[20vw] w-full min-w-[40rem]"
        },
        {
            name: instance?.name || "",
            description: instance?.description || "",
            requiresAuth: isNewInstance && requiresAuth
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
