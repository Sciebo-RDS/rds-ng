import { WebComponent } from "../../component/WebComponent";

function messageDialog(comp: WebComponent, title: string, message: string, icon: string, background: string): void {
    const confirm = comp.vue.config.globalProperties.$confirm;

    confirm.require({
        group: "messagedlg",
        header: title,
        message: message,
        icon: icon,
        background: background,
    });
}

/**
 * Shows an information message (popup) dialog.
 *
 * @param comp - The global component.
 * @param title - The dialog title.
 * @param message - The message.
 */
export function infoMessageDialog(comp: WebComponent, title: string, message: string): void {
    messageDialog(comp, title, message, "material-icons-outlined mi-info", "r-primary-bg");
}

/**
 * Shows a warning message (popup) dialog.
 *
 * @param comp - The global component.
 * @param title - The dialog title.
 * @param message - The message.
 */
export function warningMessageDialog(comp: WebComponent, title: string, message: string): void {
    messageDialog(comp, title, message, "material-icons-outlined mi-error-outline", "r-bg-warning");
}

/**
 * Shows an error message (popup) dialog.
 *
 * @param comp - The global component.
 * @param title - The dialog title.
 * @param message - The message.
 */
export function errorMessageDialog(comp: WebComponent, title: string, message: string): void {
    messageDialog(comp, title, message, "material-icons-outlined mi-error", "r-bg-error");
}
