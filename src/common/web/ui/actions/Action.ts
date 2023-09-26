import { Channel } from "../../core/messaging/Channel";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { MessageComposer } from "../../core/messaging/composers/MessageComposer";
import { Message } from "../../core/messaging/Message";
import { networkStore } from "../../data/stores/NetworkStore";
import { Service } from "../../services/Service";

export type ActionCallback<MsgType extends Message, CompType extends MessageComposer<MsgType>> = (composer: CompType) => void;

/**
 * Base class for actions from the user interface (usually but not necessarily initiated by the user). An action is a UI-extended
 * wrapper around messages.
 *
 * Note that there is no ``CommandReplyAction``, since replies are only ever sent during execution of a command.
 */
export abstract class Action<MsgType extends Message, CompType extends MessageComposer<MsgType>> {
    private readonly _service: Service;
    private readonly _serverChannel: Channel;

    private _executed = false;

    /**
     * @param service - The service to use for message emission.
     */
    public constructor(service: Service) {
        const nwStore = networkStore();

        this._service = service;
        this._serverChannel = nwStore.serverChannel;
    }

    protected executeAction(composer: CompType, callback: ActionCallback<MsgType, CompType> | null): void {
        if (this._executed) {
            throw new Error("Tried to execute an action more than once");
        }

        if (callback) {
            callback(composer);
        }

        composer.emit(this._serverChannel);

        this._executed = true;
    }

    protected get messageBuilder(): MessageBuilder {
        return this._service.messageBuilder;
    }
}
