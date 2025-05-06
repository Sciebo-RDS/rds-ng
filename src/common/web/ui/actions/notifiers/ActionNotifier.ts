import { ActionState } from "../ActionBase";

/**
 * A snap-in for actions to display arbitrary notifications about the action execution.
 */
export abstract class ActionNotifier {
    public static readonly MessagePlaceholder = "$MSG$";

    /**
     * Called when the action triggers its notification.
     */
    public onNotify(message: string = ""): void {
    }

    /**
     * Called when the action has finished (independent of its success).
     */
    public onFinished(): void {
    }

    protected formatMessage(displayMessage: string, message: string): string {
        return displayMessage.replace(ActionNotifier.MessagePlaceholder, message);
    }
}

export type ActionNotifiers = Record<ActionState, ActionNotifier[]>;
