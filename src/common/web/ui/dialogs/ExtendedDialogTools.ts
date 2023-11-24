import { toTypedSchema } from "@vee-validate/yup";
import { useForm } from "vee-validate";
import { inject, reactive, nextTick } from "vue";
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
            // @ts-ignore
            function selectFirstError({ errors }) {
                try {
                    const firstError = Object.keys(errors)[0];
                    const el = document.querySelector(`[name="${firstError}"]`) as HTMLInputElement;
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

    function useValidator<SchemaType>(schema: SchemaType, validateImmediately: boolean = true) {
        const validator = reactive(new ExtendedDialogValidator(
            useForm({
                // @ts-ignore
                validationSchema: toTypedSchema(yobject(schema))
            })
        ));

        // @ts-ignore
        dialogData.validator = validator;

        if (validateImmediately) {
            // Schedule an automatic validation for the next tick
            nextTick(() => {
                dialogData.validator?.validate().then();
            }).then();
        }

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
