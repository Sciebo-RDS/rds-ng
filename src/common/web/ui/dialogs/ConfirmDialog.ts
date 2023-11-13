import { type ConfirmationOptions } from "primevue/confirmationoptions";

import { WebComponent } from "../../component/WebComponent";

/**
 * The result of a confirmation dialog in form of a `Promise`.
 */
export type ConfirmDialogResult = Promise<void>;

/**
 * Shows a confirmation (popup) dialog.
 *
 * @param comp - The global component.
 * @param options - Confirmation dialog options; note that the `accept` and `reject` callbacks are handled through the returned ``Promise``.
 * @param ignoreReject - If true, nothing will happen if the user rejects the dialog.
 */
export function confirmDialog(comp: WebComponent, options: ConfirmationOptions, ignoreReject: boolean = true): ConfirmDialogResult {
    const confirm = comp.vue.config.globalProperties.$confirm;

    return new Promise<void>((resolve, reject) => {
        options.accept = () => {
            resolve();
        };

        if (!ignoreReject) {
            options.reject = () => {
                reject();
            };
        }

        confirm.require(options);
    });
}
