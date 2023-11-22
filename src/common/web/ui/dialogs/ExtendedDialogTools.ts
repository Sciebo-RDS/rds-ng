import { inject } from "vue";

import { type ExtendedDialogData } from "./ExtendedDialog";

/**
 * Tools for working with the extended dialog.
 */
export function extendedDialogTools() {
    const dialogRef = inject("dialogRef") as any;
    const dialogData = dialogRef.value.data as ExtendedDialogData<any>;

    function acceptDialog(): void {
        if (dialogData.accept) {
            dialogData.accept(dialogData.userData);
        }
        dialogRef.value.close(dialogData.userData);
    }

    function rejectDialog(): void {
        if (dialogData.reject) {
            dialogData.reject();
        }
        dialogRef.value.close();
    }

    return {
        dialogRef,
        dialogData,
        acceptDialog,
        rejectDialog
    };
}
