import { inject } from "vue";

import { type EditDialogData } from "./EditDialog";

/**
 * Data and functions for handling the edit dialog.
 */
export function editDialogHandling() {
    const dialogRef = inject("dialogRef") as any;
    const dialogData = dialogRef.value.data as EditDialogData<any>;

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
