import { ActionBase, ActionState } from "./ActionBase";
import { CallbackNotifier } from "./notifiers/CallbackNotifier";

/**
 * An action that encapsulates multiple other actions that are executed in order.
 */
export class MultiAction extends ActionBase {
    private readonly _actions: ActionBase[] = [] as ActionBase[];
    private _currentAction: number = -1;

    /**
     * Enqueues new actions.
     *
     * Note that actions are executed synchronously in the order in which they were added.
     *
     * @param actions - The actions to add.
     */
    public addActions(actions: ActionBase[]): void {
        this._actions.push(...actions);

        actions.forEach((action) => {
            action.addNotifier(
                ActionState.Done,
                new CallbackNotifier((message) => this.onActionDone(action, message))
            );
            action.addNotifier(
                ActionState.Failed,
                new CallbackNotifier((message) => this.onActionFailed(action, message))
            );
        });
    }

    /**
     * Executes the action (i.e., all enqueued messages will be executed).
     */
    public execute(): void {
        if (this._actions.length == 0) {
            throw new Error("Tried to execute a multi-action that doesn't contain any actions");
        }
        if (this._state != ActionState.Pending) {
            throw new Error("Tried to execute an action more than once");
        }

        this.setState(ActionState.Executing);

        this.preExecution();
        this.executeNextAction();
        this.postExecution();
    }

    private executeNextAction(): void {
        // If a next action is still available, execute it; otherwise, this action is done
        if (++this._currentAction < this._actions.length) {
            this._actions[this._currentAction].execute();
        } else {
            this.setState(ActionState.Done);
        }
    }

    private onActionDone(action: ActionBase, message: string): void {
        this.executeNextAction();
    }

    private onActionFailed(action: ActionBase, message: string): void {
        this.setState(ActionState.Failed, message);
    }
}
