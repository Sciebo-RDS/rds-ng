import { type ToastServiceMethods } from "primevue/toastservice";

import { WebComponent } from "../../component/WebComponent";
import { GeneralSettingIDs } from "../../settings/GeneralSettingIDs";

/**
 * The type of an overlay notification.
 */
export const enum OverlayNotificationType {
    Info = "info",
    Success = "success",
    Warning = "warn",
    Error = "error",
}

/**
 * A helper class to display notifications using PrimeVue's Toast.
 */
export class OverlayNotifications {
    private readonly _toast: ToastServiceMethods;
    private readonly _timeout: number;

    /**
     * @param comp - The global component.
     */
    public constructor(comp: WebComponent) {
        this._toast = comp.vue.config.globalProperties.$toast;

        this._timeout = comp.data.config.value<number>(GeneralSettingIDs.NotificationTimeout) * 1000;
    }

    /**
     * Display an info notification.
     *
     * @param caption - The notification caption.
     * @param message - The notification message.
     * @param sticky - Whether the notification will be sticky.
     */
    public info(caption: string, message: string, sticky: boolean = false): void {
        this.notify(OverlayNotificationType.Info, caption, message, sticky);
    }

    /**
     * Display a success notification.
     *
     * @param caption - The notification caption.
     * @param message - The notification message.
     * @param sticky - Whether the notification will be sticky.
     */
    public success(caption: string, message: string, sticky: boolean = false): void {
        this.notify(OverlayNotificationType.Success, caption, message, sticky);
    }

    /**
     * Display a warning notification.
     *
     * @param caption - The notification caption.
     * @param message - The notification message.
     * @param sticky - Whether the notification will be sticky.
     */
    public warning(caption: string, message: string, sticky: boolean = false): void {
        this.notify(OverlayNotificationType.Warning, caption, message, sticky);
    }

    /**
     * Display an error notification.
     *
     * @param caption - The notification caption.
     * @param message - The notification message.
     * @param sticky - Whether the notification will be sticky.
     */
    public error(caption: string, message: string, sticky: boolean = false): void {
        this.notify(OverlayNotificationType.Error, caption, message, sticky);
    }

    /**
     * Display a notification.
     *
     * @param type - The notification type.
     * @param caption - The notification caption.
     * @param message - The notification message.
     * @param sticky - Whether the notification will be sticky.
     */
    public notify(type: OverlayNotificationType, caption: string, message: string, sticky: boolean): void {
        this._toast.add({
            severity: type,
            summary: caption,
            detail: message,
            life: sticky ? 0 : this._timeout,
        });
    }
}
