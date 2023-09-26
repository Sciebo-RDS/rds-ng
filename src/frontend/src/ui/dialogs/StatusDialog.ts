import { Dialog } from "@common/ui/dialogs/Dialog";

import StatusDialogTemplate from "@/ui/dialogs/StatusDialog.vue";

/**
 * A simple non-closable status dialog.
 */
export class StatusDialog extends Dialog {
    /**
     * Shows the dialog.
     *
     * @param caption - The header caption.
     * @param status - The status text.
     * @param icon - An optional icon.
     */
    public show(caption: string, status: string, icon: string = ""): void {
        this.showDialog(StatusDialogTemplate, {
            props: {
                header: caption,
                modal: true,
                closable: false,
                draggable: false,
            },
            data: {
                status: status,
                icon: icon,
            }
        });
    }

    /**
     * Hides the dialog.
     */
    public hide() {
        this.hideDialog();
    }
}
