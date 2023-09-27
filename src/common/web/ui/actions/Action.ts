import { Channel } from "../../core/messaging/Channel";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { MessageComposer } from "../../core/messaging/composers/MessageComposer";
import { Message } from "../../core/messaging/Message";
import { networkStore } from "../../data/stores/NetworkStore";
import { Service } from "../../services/Service";
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
 * Base class for actions from the user interface (usually but not necessarily initiated by the user). An action is a UI-extended
 * wrapper around messages.
 *
 * Note that there is no ``CommandReplyAction``, since replies are only ever sent during execution of a command.
 */
export abstract class Action<MsgType extends Message, CompType extends MessageComposer<MsgType>> {
    private readonly _service: Service;
    private readonly _serverChannel: Channel;

    private _state: ActionState;
    private readonly _notifiers: ActionNotifiers = {};

    protected _composer: CompType | null = null;

    /**
     * @param service - The service to use for message emission.
     */
    public constructor(service: Service) {
        const nwStore = networkStore();

        this._service = service;
        this._serverChannel = nwStore.serverChannel;

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
        this._notifiers[state].push(notifier);
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

        if (state == ActionState.Done || state == ActionState.Failed) {
            // All notifiers need to know when the action has finished
            for (const [_, notifiers] of Object.entries(this._notifiers)) {
                notifiers.forEach((notifier: ActionNotifier) => {
                    notifier.onFinished();
                })
            }
        }

        if (state in this._notifiers) {
            this._notifiers[state].forEach((notifer: ActionNotifier) => {
                notifer.onNotify(message);
            });
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
