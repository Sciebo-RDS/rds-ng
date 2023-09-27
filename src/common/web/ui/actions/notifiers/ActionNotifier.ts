/**
 * A snap-in for actions to display arbitrary notifications about the action execution.
 */
export abstract class ActionNotifier {
    /**
     * Called when the action is being executed.
     */
    public onExecute(): void {
    }

    /**
     * Called when the action has finished (independent of its success).
     */
    public onFinished(): void {
    }

    /**
     * Called when the action succeeded.
     */
    public onDone(): void {
    }

    /**
     * Called when the action failed.
     *
     * @param reason - The failure reason.
     */
    public onFailed(reason: string): void {
    }
}
