import { WebComponent } from "../../../component/WebComponent";
import { OverlayNotifications, OverlayNotificationType } from "../../notifications/OverlayNotifications";
import { ActionNotifier } from "./ActionNotifier";

/**
 * Notifications displayed via status messages.
 */
export class StatusNotifier extends ActionNotifier {
    private readonly _type: OverlayNotificationType;
    private readonly _message: string;
    private readonly _icon: string;
    private readonly _sticky: boolean;

    /**
     * @param type - The notification type.
     * @param message - The message.
     * @param icon - The message icon.
     * @param sticky - Whether the notification will be sticky.
     */
    public constructor(type: OverlayNotificationType, message: string, icon: string, sticky: boolean = false) {
        super();

        this._type = type;
        this._message = message;
        this._icon = icon;
        this._sticky = sticky;
    }

    public onNotify(message: string): void {
        const notifications = new OverlayNotifications(WebComponent.instance);
        notifications.clearStatus();
        notifications.notifyStatus(this._type, this.formatMessage(this._message, message), this._icon, this._sticky);
    }
}
