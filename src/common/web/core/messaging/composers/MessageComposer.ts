import { UnitID } from "../../../utils/UnitID";
import { Channel } from "../Channel";
import { type ConstructableMessage, Message } from "../Message";
import { type MessageBusProtocol } from "../MessageBusProtocol";
import { type Payload, PayloadData } from "../MessagePayload";
import { MessageMetaInformation } from "../meta/MessageMetaInformation";

export type BeforeDispatchCallback = (msg: Message, msgMeta: MessageMetaInformation) => void;

/**
 * A class to collect all information necessary to create and emit a message.
 */
export abstract class MessageComposer<MsgType extends Message> {
    protected _originID: UnitID;
    protected _messageBus: MessageBusProtocol;

    protected _msgType: ConstructableMessage<MsgType>;
    protected _params: Record<string, any>;
    protected _payload: Payload = {};
    protected _chain: Message | null;

    private _beforeCallbacks: BeforeDispatchCallback[] = [];

    /**
     * @param originID - The component identifier of the origin of newly created messages.
     * @param messageBus - The global message bus to use.
     * @param msgType - The message type.
     * @param params - Additional message parameters.
     * @param chain - A message that acts as the *predecessor* of the new message. Used to keep the same trace for multiple messages.
     */
    public constructor(
        originID: UnitID,
        messageBus: MessageBusProtocol,
        msgType: ConstructableMessage<MsgType>,
        params: Record<string, any> = {},
        chain: Message | null = null
    ) {
        this._originID = originID;
        this._messageBus = messageBus;

        this._msgType = msgType;
        this._params = params;
        this._chain = chain;
    }

    /**
     * Adds a payload item to the message.
     *
     * @param key - The item key.
     * @param data - The item data.
     */
    public addPayload(key: string, data: PayloadData): void {
        this._payload[key] = data;
    }

    /**
     * Adds a callback that will be called immediately before the message is dispatched.
     *
     * @param cb - The callback to add.
     *
     * @returns - This composer instance to allow call chaining.
     */
    public before(cb: BeforeDispatchCallback): this {
        this._beforeCallbacks.push(cb);
        return this;
    }

    /**
     * Sends the built message through the message bus.
     *
     * @param target - The target of the message.
     */
    public emit(target: Channel): void {
        this.verify();
        this.compose();

        let msgMeta = this.createMetaInformation();
        let msg = this.createMessage(target);

        for (const cb of this._beforeCallbacks) {
            cb(msg, msgMeta);
        }

        this._messageBus.dispatch(msg, msgMeta);
    }

    protected verify(): void {}

    protected compose(): void {}

    protected abstract createMetaInformation(): MessageMetaInformation;

    private createMessage(target: Channel): Message {
        let msg = this._chain
            ? new this._msgType(this._originID, this._originID, target, [this._originID], this._chain.trace)
            : new this._msgType(this._originID, this._originID, target, [this._originID]);

        for (const [key, value] of Object.entries(this._params)) {
            if (key in msg) {
                msg[key as keyof MsgType] = value;
            } else {
                throw new Error(`Provided unknown value '${key}' for message type ${msg.name}`);
            }
        }
        msg.payload.decode(this._payload);
        return msg;
    }
}
