import { WebComponent } from "@common/component/WebComponent";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";

import { MessageDialog } from "@/ui/dialogs/MessageDialog";

/**
 * Notifications displayed via dialogs.
 */
export class DialogNotifier extends ActionNotifier {
    private readonly _caption: string;
    private readonly _message: string;
    private readonly _icon: string;
    private readonly _autoClose: boolean;

    private _dialog: MessageDialog | null = null;

    /**
     * @param caption - The caption.
     * @param message - The message.
     * @param icon - An optional icon name.
     * @param autoClose - Whether the dialog automatically closes once the action has finished.
     */
    public constructor(caption: string, message: string, icon: string = "", autoClose: boolean = false) {
        super();

        this._caption = caption;
        this._message = message;
        this._icon = icon;
        this._autoClose = autoClose;
    }

    public onNotify(message: string): void {
        this._dialog = new MessageDialog(WebComponent.instance);
        this._dialog.show(this._caption, this.formatMessage(this._message, message), this._icon, !this._autoClose);
    }

    public onFinished(): void {
        if (this._autoClose) {
            this._dialog?.hide();
        }
    }
}
