import { markRaw } from "vue";

import { Dialog } from "@common/ui/dialogs/Dialog";

import MessageDialogBody from "@/ui/dialogs/MessageDialog.vue";
import MessageDialogFooter from "@/ui/dialogs/MessageDialogFooter.vue";

/**
 * A simple message dialog.
 */
export class MessageDialog extends Dialog {
    /**
     * Shows the dialog.
     *
     * @param caption - The header caption.
     * @param message - The message text.
     * @param icon - An optional icon.
     * @param closable - Whether the dialog is closable.
     */
    public show(caption: string, message: string, icon: string = "", closable: boolean = true): void {
        let options = {
            props: {
                header: caption,
                modal: true,
                closable: closable,
                draggable: false,
            },
            data: {
                message: message,
                icon: icon,
            },
            templates: {}
        };

        if (closable) {
            options.templates = {
                footer: markRaw(MessageDialogFooter)
            }
        }

        this.showDialog(MessageDialogBody, options);
    }

    /**
     * Hides the dialog.
     */
    public hide() {
        this.hideDialog();
    }
}
