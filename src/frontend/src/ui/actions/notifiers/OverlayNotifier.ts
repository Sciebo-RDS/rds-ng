import { WebComponent } from "@common/component/WebComponent";
import { ActionNotifier } from "@common/ui/actions/notifiers/ActionNotifier";
import { OverlayNotifications, OverlayNotificationType } from "@common/ui/notifications/OverlayNotifications";

/**
 * Notifications displayed via overlay messages.
 */
export class OverlayNotifier extends ActionNotifier {
    private readonly _type: OverlayNotificationType;
    private readonly _caption: string;
    private readonly _message: string;
    private readonly _sticky: boolean;

    /**
     * @param type - The notification type.
     * @param caption - The caption.
     * @param message - The message.
     * @param sticky - Whether the notification will be sticky.
     */
    public constructor(type: OverlayNotificationType, caption: string, message: string, sticky: boolean = false) {
        super();

        this._type = type;
        this._caption = caption;
        this._message = message;
        this._sticky = sticky;
    }

    public onNotify(message: string): void {
        const notifications = new OverlayNotifications(WebComponent.instance);
        notifications.notify(this._type, this._caption, this.formatMessage(this._message, message), this._sticky);
    }
}
