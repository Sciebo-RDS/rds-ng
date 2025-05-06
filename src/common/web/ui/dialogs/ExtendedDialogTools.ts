import { inject, reactive } from "vue";
import * as yup from "yup";

import { scrollElementIntoView } from "../../utils/HTMLUtils";

import { type ExtendedDialogData } from "./ExtendedDialog";
import { ExtendedDialogValidator } from "./ExtendedDialogValidator";

/**
 * Tools for working with the extended dialog.
 */
export function useExtendedDialogTools() {
    const dialogRef = inject("dialogRef") as any;
    const dialogData = dialogRef.value.data as ExtendedDialogData<any>;

    function acceptDialog(): void {
        function accept() {
            if (dialogData.accept) {
                dialogData.accept(dialogData.userData);
            }
            dialogRef.value.close(dialogData.userData);
        }

        if (dialogData.processData) {
            dialogData.processData(dialogData.userData);
        }

        if (dialogData.validator) {
            function selectFirstError(errors: yup.ValidationError[]) {
                try {
                    const firstError = errors[0];
                    scrollElementIntoView(`[name="${firstError.path}"]`);
                } catch (e) {}
            }

            dialogData.validator
                .validate()
                .then(() => {
                    accept();
                })
                .catch((errors: yup.ValidationError[]) => {
                    selectFirstError(errors);
                });
        } else {
            accept();
        }
    }

    function rejectDialog(): void {
        if (dialogData.reject) {
            dialogData.reject();
        }
        dialogRef.value.close();
    }

    function useValidator<FormType, ShapeType extends yup.ObjectShape>(form: FormType, shape: ShapeType) {
        const validator = reactive(new ExtendedDialogValidator(form, shape));

        // @ts-ignore
        dialogData.validator = validator;
        return validator;
    }

    return {
        dialogRef,
        dialogData,
        acceptDialog,
        rejectDialog,
        useValidator
    };
}
