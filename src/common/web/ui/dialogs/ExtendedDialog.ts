import { type DialogProps } from "primevue/dialog";
import { type DynamicDialogOptions } from "primevue/dynamicdialogoptions";
import { markRaw } from "vue";

import { type VueComponent, WebComponent } from "../../component/WebComponent";

import { ExtendedDialogValidator } from "./ExtendedDialogValidator";

import ExtendedDialogFooter from "./ExtendedDialogFooter.vue";

/**
 * Various display options of the extended dialog.
 */
export interface ExtendedDialogOptions {
    /** Whether the dialog has an Accept button. */
    hasAcceptButton?: boolean;
    /** The label of the Accept button */
    acceptLabel?: string;
    /** The icon of the Accept button */
    acceptIcon?: string;

    /** Whether the dialog has a Reject button. */
    hasRejectButton?: boolean;
    /** The label of the Reject button */
    rejectLabel?: string;
    /** The icon of the Reject button */
    rejectIcon?: string;
}

/**
 * Data for dynamic extended dialogs.
 */
export interface ExtendedDialogData<UserDataType> {
    /** Custom user data. */
    userData: UserDataType;

    /** Various display properties */
    options: ExtendedDialogOptions;

    /** A form validator if a schema was provided in the options. */
    validator?: ExtendedDialogValidator<any>;

    /** Called when the dialog was accepted. */
    accept?: (data: UserDataType) => void;

    /** Called when the dialog was dismissed. */
    reject?: () => void;
}

/**
 * The result of an extended dialog in form of a `Promise`.
 */
export type ExtendedDialogResult<ResultType> = Promise<ResultType>;

/**
 * Shows a (popup) dialog with extended functionality.
 *
 * @param comp - The global component.
 * @param dialogComponent - The main dialog component to load.
 * @param dialogProps - Vue dialog properties.
 * @param data - Optional user data to pass to the dialog.
 * @param options - Extended dialog options.
 * @param ignoreReject - If true, nothing will happen if the user rejects the dialog.
 */
export function extendedDialog<DataType>(
    comp: WebComponent,
    dialogComponent: VueComponent,
    dialogProps: DialogProps,
    data: DataType,
    options: ExtendedDialogOptions | undefined = undefined,
    ignoreReject: boolean = true
): ExtendedDialogResult<DataType> {
    const dialog = comp.vue.config.globalProperties.$dialog;

    return new Promise<DataType>((resolve, reject) => {
        const dialogData: ExtendedDialogData<DataType> = {
            userData: data,
            options: options || {} as ExtendedDialogOptions
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
            props: dialogProps,
            templates: {
                footer: markRaw(ExtendedDialogFooter)
            },
            data: dialogData
        };

        dialog.open(dialogComponent, dialogOptions);
    });
}
