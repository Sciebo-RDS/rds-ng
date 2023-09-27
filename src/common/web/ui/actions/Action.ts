import { Channel } from "../../core/messaging/Channel";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { MessageComposer } from "../../core/messaging/composers/MessageComposer";
import { Message } from "../../core/messaging/Message";
import { networkStore } from "../../data/stores/NetworkStore";
import { Service } from "../../services/Service";
import { ActionNotifier } from "./notifiers/ActionNotifier";

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
 * Base class for actions from the user interface (usually but not necessarily initiated by the user). An action is a UI-extended
 * wrapper around messages.
 *
 * Note that there is no ``CommandReplyAction``, since replies are only ever sent during execution of a command.
 */
export abstract class Action<MsgType extends Message, CompType extends MessageComposer<MsgType>> {
    private readonly _service: Service;
    private readonly _serverChannel: Channel;

    private _state: ActionState;
    private readonly _notifiers: ActionNotifier[];

    protected _composer: CompType | null = null;

    /**
     * @param service - The service to use for message emission.
     * @param notifiers - Action notifiers.
     */
    public constructor(service: Service, notifiers: ActionNotifier[] = []) {
        const nwStore = networkStore();

        this._service = service;
        this._serverChannel = nwStore.serverChannel;

        this._state = ActionState.Pending;
        this._notifiers = notifiers;
    }

    /**
     * Prepares this action.
     *
     * @returns - A message composer that can be further modified.
     */
    public abstract prepare(...args: any[]): CompType;

    /**
     * Executes the action (i.e., the message will be emitted).
     */
    public execute(): void {
        if (this._state != ActionState.Pending) {
            throw new Error("Tried to execute an action more than once");
        }
        if (!this._composer) {
            throw new Error("Tried to execute an action before preparing it");
        }

        this.setState(ActionState.Executing);

        this.preExecution();
        this._composer.emit(this._serverChannel);
        this.postExecution();
    }

    protected preExecution(): void {
    }

    protected postExecution(): void {
    }

    protected setState(state: ActionState, message: string = ""): void {
        this._state = state;

        for (const notifier of this._notifiers) {
            switch (this._state) {
                case ActionState.Executing:
                    notifier.onExecute();
                    break;
                case ActionState.Done:
                    notifier.onFinished();
                    notifier.onDone();
                    break;
                case ActionState.Failed:
                    notifier.onFinished();
                    notifier.onFailed(message);
                    break;
            }
        }
    }

    /**
     * The current state of the action.
     */
    public get state(): ActionState {
        return this._state;
    }

    protected get messageBuilder(): MessageBuilder {
        return this._service.messageBuilder;
    }
}
