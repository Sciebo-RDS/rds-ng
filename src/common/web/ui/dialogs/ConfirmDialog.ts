import { ConfirmationOptions } from "primevue/confirmationoptions";

import { WebComponent } from "../../component/WebComponent";

/**
 * Shows a confirmation (popup) dialog.
 *
 * @param comp - The global component.
 * @param options - Confirmation dialog options; note that the `accept` and `reject` callbacks are handled through the returned ``Promise``.
 */
export function confirmDialog(comp: WebComponent, options: ConfirmationOptions): Promise<void> {
    const confirm = comp.vue.config.globalProperties.$confirm;

    return new Promise<void>((resolve, reject) => {
        confirm.require({
            ...options,
            accept: () => {
                resolve();
            },
            reject: () => {
                reject();
            },
        });
    });
}
