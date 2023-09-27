import { WebComponent } from "@common/component/WebComponent";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";

import { MessageDialog } from "@/ui/dialogs/MessageDialog";

export class ExecutionDialogNotifier extends ActionNotifier {
    private readonly _caption: string;
    private readonly _message: string;
    private readonly _icon: string;

    private _dialog: MessageDialog | null = null;

    public constructor(caption: string, message: string, icon: string = "") {
        super();

        this._caption = caption;
        this._message = message;
        this._icon = icon;
    }

    public onExecute(): void {
        this._dialog = new MessageDialog(WebComponent.instance);
        this._dialog.show(this._caption, this._message, this._icon, false);
    }

    public onFinished(): void {
        this._dialog?.hide();
    }
}
