import { ActionNotifier } from "./ActionNotifier";

export type NotifierCallback = (message: string) => void;

/**
 * A simple action notifier that calls a callback function on notification.
 */
export class CallbackNotifier extends ActionNotifier {
    private readonly _callback: NotifierCallback;

    public constructor(callback: NotifierCallback) {
        super();

        this._callback = callback;
    }

    public onNotify(message: string): void {
        this._callback(message);
    }
}
