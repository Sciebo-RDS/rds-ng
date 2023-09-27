import { WebComponent } from "@common/component/WebComponent";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";

import { MessageDialog } from "@/ui/dialogs/MessageDialog";

export class ErrorDialogNotifier extends ActionNotifier {
    private readonly _caption: string;
    private readonly _message: string;

    public constructor(caption: string, message: string) {
        super();

        this._caption = caption;
        this._message = message;
    }

    public onFailed(reason: string): void {
        const msgDlg = new MessageDialog(WebComponent.instance);
        msgDlg.show(this._caption, `${this._message}:\n${reason}`, "error");
    }
}
