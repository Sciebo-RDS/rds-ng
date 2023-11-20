import { type DialogProps } from "primevue/dialog";
import { type DynamicDialogOptions } from "primevue/dynamicdialogoptions";
import { type Component as VueComponent, markRaw } from "vue";

import { WebComponent } from "../../component/WebComponent";

import EditDialogFooter from "./EditDialogFooter.vue";

/**
 * Data for dynamic edit dialogs.
 */
export interface EditDialogData<UserDataType> {
    /** Custom user data. */
    userData: UserDataType;

    /** Called when the dialog was accepted. */
    accept?: (data: UserDataType) => void;

    /** Called when the dialog was dismissed. */
    reject?: () => void;
}

/**
 * The result of an edit dialog in form of a `Promise`.
 */
export type EditDialogResult<ResultType> = Promise<ResultType>;

/**
 * Shows a (popup) dialog for editing.
 *
 * @param comp - The global component.
 * @param dialogComponent - The main dialog component to load.
 * @param options - Edit dialog options.
 * @param data - Optional user data to pass to the dialog.
 * @param ignoreReject - If true, nothing will happen if the user rejects the dialog.
 */
export function editDialog<DataType>(comp: WebComponent, dialogComponent: VueComponent, options: DialogProps, data: DataType, ignoreReject: boolean = true): EditDialogResult<DataType> {
    const dialog = comp.vue.config.globalProperties.$dialog;

    // TODO: Enter/Escape handlen
    return new Promise<DataType>((resolve, reject) => {
        const dialogData: EditDialogData<DataType> = {
            userData: data
        };

        dialogData.accept = (result: DataType) => {
            resolve(result);
        };

        if (!ignoreReject) {
            dialogData.reject = () => {
                reject();
            };
        }

        const dialogOptions: DynamicDialogOptions = {
            props: options,
            templates: {
                footer: markRaw(EditDialogFooter)
            },
            data: dialogData
        };

        dialog.open(dialogComponent, dialogOptions);
    });
}
