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
    /** If true, closing the dialog always will accept it. */
    acceptOnClose?: boolean;

    /** Whether the dialog has a Reject button. */
    hasRejectButton?: boolean;
    /** The label of the Reject button */
    rejectLabel?: string;
    /** The icon of the Reject button */
    rejectIcon?: string;

    /** Additional options. */
    [key: string]: any;
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

    /** Called before accepting the dialog to pre-process the dialog data. */
    processData?: (data: UserDataType) => void;

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
 * @param processDataCallback - A callback that is called before the dialog is being accepted to pre-process the dialog data.
 * @param ignoreReject - If true, nothing will happen if the user rejects the dialog.
 */
export function extendedDialog<UserDataType>(
    comp: WebComponent,
    dialogComponent: VueComponent,
    dialogProps: DialogProps,
    data: UserDataType,
    options: ExtendedDialogOptions | undefined = undefined,
    processDataCallback: ((data: UserDataType) => void) | undefined = undefined,
    ignoreReject: boolean = true,
): ExtendedDialogResult<UserDataType> {
    const dialog = comp.vue.config.globalProperties.$dialog;

    return new Promise<UserDataType>((resolve, reject) => {
        const dialogData: ExtendedDialogData<UserDataType> = {
            userData: data,
            options: options || ({} as ExtendedDialogOptions),
            processData: processDataCallback,
        };

        dialogData.accept = (result: UserDataType) => {
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
                footer: markRaw(ExtendedDialogFooter),
            },
            data: dialogData,
        };

        if (dialogData.options.acceptOnClose) {
            dialogOptions.onClose = () => {
                if (dialogData.processData) {
                    dialogData.processData(dialogData.userData);
                }

                resolve(dialogData.userData);
            };
        }

        dialog.open(dialogComponent, dialogOptions);
    });
}
