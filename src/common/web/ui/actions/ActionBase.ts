import { WebComponent } from "../../component/WebComponent";
import { GeneralSettingIDs } from "../../settings/GeneralSettingIDs";
import { ExecutionCallbacks } from "../../utils/ExecutionCallbacks";
import { ActionNotifier, type ActionNotifiers } from "./notifiers/ActionNotifier";

/**
 * The state in which an action can be.
 */
export const enum ActionState {
    Pending,
    Executing,
    Done,
    Failed,
}

export type ActionDoneCallback = () => void;
export type ActionFailCallback = () => void;

/**
 * Abstract base class for general actions.
 */
export abstract class ActionBase {
    protected _state: ActionState;

    private readonly _stateCallbacks = new ExecutionCallbacks<ActionDoneCallback, ActionFailCallback>();

    private readonly _notifiers: ActionNotifiers = {} as ActionNotifiers;
    private readonly _suppressDefaultNotifiers: boolean;

    /**
     * @param suppressDefaultNotifiers - Suppress default notifiers.
     */
    public constructor(suppressDefaultNotifiers: boolean = false) {
        this._state = ActionState.Pending;

        this._suppressDefaultNotifiers = suppressDefaultNotifiers;
    }

    /**
     * Adds a callback for action completion.
     *
     * @param cb - The callback to add.
     */
    public completed(cb: ActionDoneCallback): this {
        this._stateCallbacks.done(cb);
        return this;
    }

    /**
     * Adds a callback for action failure.
     *
     * @param cb - The callback to add.
     */
    public failed(cb: ActionFailCallback): this {
        this._stateCallbacks.failed(cb);
        return this;
    }

    /**
     * Adds a new notifier for the specified state.
     *
     * @param state - The state the notifier should react to.
     * @param notifier - The notifier.
     * @param debugOnly - If true, the notification will only be added in debug mode.
     */
    public addNotifier(state: ActionState, notifier: ActionNotifier | ActionNotifier[], debugOnly: boolean = false): void {
        if (debugOnly) {
            if (!WebComponent.instance.data.config.value<boolean>(GeneralSettingIDs.Debug)) {
                return;
            }
        }

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

    protected addDefaultNotifiers(...args: any[]): void {}

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

        if (state == ActionState.Done) {
            this._stateCallbacks.invokeDoneCallbacks();
        } else if (state == ActionState.Failed) {
            this._stateCallbacks.invokeFailCallbacks();
        }

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

    protected onStateChanged(newState: ActionState, oldState: ActionState): void {}

    protected preExecution(): void {}

    protected postExecution(): void {}

    /**
     * The current state of the action.
     */
    public get state(): ActionState {
        return this._state;
    }
}
