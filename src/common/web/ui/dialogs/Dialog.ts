import { type DynamicDialogInstance, type DynamicDialogOptions } from "primevue/dynamicdialogoptions";
import { type App } from "vue";

import { WebComponent } from "../../component/WebComponent";

/**
 * A helper class to handle dynamic dialogs.
 */
export class Dialog {
    private readonly _vue: App;

    private _dialog: DynamicDialogInstance | null = null;

    /**
     * @param comp - The global component.
     */
    public constructor(comp: WebComponent) {
        this._vue = comp.vue;
    }

    /**
     * Shows a dynamic dialog.
     *
     * @param content - The content Vue component.
     * @param options - Dialog options.
     */
    public showDialog(content: any, options: DynamicDialogOptions): void {
        const dialog = this._vue.config.globalProperties.$dialog;
        this._dialog = dialog.open(content, {
            ...options,
            onClose: () => {
                this._dialog = null;
            }
        });
    }

    /**
     * Hides the current dialog.
     */
    public hideDialog(): void {
        this._dialog?.close();
    }
}
