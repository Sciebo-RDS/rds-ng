import { Channel } from "../../core/messaging/Channel";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { MessageComposer } from "../../core/messaging/composers/MessageComposer";
import { Message } from "../../core/messaging/Message";
import { useNetworkStore } from "../../data/stores/NetworkStore";
import { Service } from "../../services/Service";
import { ActionBase, ActionState } from "./ActionBase";

/**
 * Base class for actions from the user interface (usually but not necessarily initiated by the user). An action is a UI-extended
 * wrapper around messages.
 *
 * Note that there is no ``CommandReplyAction``, since replies are only ever sent during execution of a command.
 */
export abstract class Action<MsgType extends Message, CompType extends MessageComposer<MsgType>> extends ActionBase {
    private readonly _service: Service;
    private readonly _serverChannel: Channel;

    protected _composer: CompType | null = null;

    /**
     * @param service - The service to use for message emission.
     * @param suppressDefaultNotifiers - Suppress default notifiers.
     */
    public constructor(service: Service, suppressDefaultNotifiers: boolean = false) {
        super(suppressDefaultNotifiers);

        const nwStore = useNetworkStore();

        this._service = service;
        this._serverChannel = nwStore.serverChannel;
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

    protected get messageBuilder(): MessageBuilder {
        return this._service.messageBuilder;
    }
}
