import { toTypedSchema } from "@vee-validate/yup";
import { useForm } from "vee-validate";
import { inject, reactive } from "vue";
import { object as yobject } from "yup";

import { type ExtendedDialogData } from "./ExtendedDialog";
import { ExtendedDialogValidator } from "./ExtendedDialogValidator";

/**
 * Tools for working with the extended dialog.
 */
export function extendedDialogTools() {
    const dialogRef = inject("dialogRef") as any;
    const dialogData = dialogRef.value.data as ExtendedDialogData<any>;

    function acceptDialog(): void {
        function accept() {
            if (dialogData.accept) {
                dialogData.accept(dialogData.userData);
            }
            dialogRef.value.close(dialogData.userData);
        }

        if (dialogData.validator) {
            function selectFirstError({ errors }) {
                try {
                    const firstError = Object.keys(errors)[0];
                    const el = document.querySelector(`[name="${firstError}"]`);
                    el?.scrollIntoView({ behavior: "smooth" });
                    el?.focus();
                } catch (e) {
                }
            }

            dialogData.validator.handleSubmit(accept, selectFirstError)();
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

    function useValidator<SchemaType, ValidatorType>(schema: SchemaType): ValidatorType {
        const validator = reactive(new ExtendedDialogValidator(
            useForm({
                validationSchema: toTypedSchema(yobject(schema))
            })
        ));

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
