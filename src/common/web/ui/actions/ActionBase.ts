import { ActionNotifier, type ActionNotifiers } from "./notifiers/ActionNotifier";

/**
 * The state in which an action can be.
 */
export const enum ActionState {
    Pending,
    Executing,
    Done,
    Failed
}

/**
 * Abstract base class for general actions.
 */
export abstract class ActionBase {
    protected _state: ActionState;

    private readonly _notifiers: ActionNotifiers = {} as ActionNotifiers;
    private _suppressDefaultNotifiers: boolean = false;

    public constructor() {
        this._state = ActionState.Pending;
    }

    /**
     * Adds a new notifier for the specified state.
     *
     * @param state - The state the notifier should react to.
     * @param notifier - The notifier.
     */
    public addNotifier(state: ActionState, notifier: ActionNotifier | ActionNotifier[]): void {
        if (!(state in this._notifiers)) {
            this._notifiers[state] = [];
        }

        if (Array.isArray(notifier)) {
            this._notifiers[state].push(...notifier);
        } else {
            this._notifiers[state].push(notifier);
        }
    }

    protected prepareNotifiers(...args: any[]): void {
        if (!this._suppressDefaultNotifiers) {
            this.addDefaultNotifiers(...args);
        }
    }

    protected addDefaultNotifiers(...args: any[]): void {
    }

    /**
     * Executes the action.
     */
    public abstract execute(): void;

    /**
     * Sets the active state of this action.
     *
     * @param state - The state to apply
     * @param message - An optional notification message.
     */
    protected setState(state: ActionState, message: string = ""): void {
        if (state == this._state) {
            return;
        }

        let oldState = this._state;
        this._state = state;
        this.onStateChanged(state, oldState);

        if (state == ActionState.Done || state == ActionState.Failed) {
            // All notifiers need to know when the action has finished
            for (const [_, notifiers] of Object.entries(this._notifiers)) {
                notifiers.forEach((notifier: ActionNotifier) => {
                    notifier.onFinished();
                });
            }
        }

        if (state in this._notifiers) {
            this._notifiers[state].forEach((notifer: ActionNotifier) => {
                notifer.onNotify(message);
            });
        }
    }

    protected onStateChanged(newState: ActionState, oldState: ActionState): void {
    }

    protected preExecution(): void {
    }

    protected postExecution(): void {
    }

    /**
     * The current state of the action.
     */
    public get state(): ActionState {
        return this._state;
    }

    /**
     * Whether default notifiers are suppressed.
     */
    public get suppressDefaultNotifiers(): boolean {
        return this._suppressDefaultNotifiers;
    }

    /**
     * Suppress default notifiers. Must be called in `prepare` is called.
     */
    public set suppressDefaultNotifiers(suppress: boolean) {
        this._suppressDefaultNotifiers = suppress;
    }
}
