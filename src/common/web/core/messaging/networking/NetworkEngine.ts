import { WebComponentData } from "../../../component/WebComponentData";
import { type Constructable } from "../../../utils/Types";
import logging from "../../logging/Logging";
import { MessageBuilder } from "../composers/MessageBuilder";
import { Command } from "../Command";
import { CommandReply } from "../CommandReply";
import { Event } from "../Event";
import { Message, type MessageCategory } from "../Message";
import { type MessageBusProtocol } from "../MessageBusProtocol";
import { type Payload } from "../MessagePayload";
import { MessageTypesCatalog } from "../MessageTypesCatalog";
import { CommandMetaInformation } from "../meta/CommandMetaInformation";
import { CommandReplyMetaInformation } from "../meta/CommandReplyMetaInformation";
import { EventMetaInformation } from "../meta/EventMetaInformation";
import { MessageEntrypoint, MessageMetaInformation } from "../meta/MessageMetaInformation";
import { Client } from "./Client";
import { NetworkRouter, NetworkRouterDirection } from "./NetworkRouter";

/**
 * Main network management class.
 *
 * Messages go out to other components through this class, and new messages come in from the outside world here as well.
 * The network engine takes care of listening to incoming messages, routing them properly, and sending new messages to other components.
 */
export class NetworkEngine {
    private readonly _compData: WebComponentData;

    private readonly _messageBus: MessageBusProtocol;

    private readonly _client: Client;
    private readonly _router: NetworkRouter;

    private readonly _metaInformationTypes: Record<MessageCategory, Constructable> = {};

    /**
     * @param compData - The global component data.
     * @param messageBus - The global message bus.
     */
    public constructor(compData: WebComponentData, messageBus: MessageBusProtocol) {
        this._compData = compData;

        this._messageBus = messageBus;

        this._client = this.createClient();
        this._router = new NetworkRouter(this._compData.compID);

        this._metaInformationTypes[Command.Category] = CommandMetaInformation;
        this._metaInformationTypes[CommandReply.Category] = CommandReplyMetaInformation;
        this._metaInformationTypes[Event.Category] = EventMetaInformation;
    }

    private createClient(): Client {
        return new Client(this._compData.compID, this._compData.config, new MessageBuilder(this._compData.compID, this._messageBus));
    }

    /**
     * Listens to incoming messages in order to properly route them.
     */
    public run(): void {
        this._client.setMessageHandler((msgName: string, data: string, payload: Payload) => {
            this.handleReceivedMessage(MessageEntrypoint.Client, msgName, data, payload);
        });

        this._client.run();
    }

    /**
     * Called to perform periodic tasks.
     */
    public process(): void {
        this._client.process();
    }

    /**
     * Sends a message across the network.
     *
     * To do so, the message is first checked for validity (whether it actually *may* be sent). If it is valid, it is routed through the
     * client (the logic of this can be found in ``NetworkRouter``).
     *
     * @param msg - The message to be sent.
     * @param msgMeta - The message meta information.
     */
    public sendMessage(msg: Message, msgMeta: MessageMetaInformation): void {
        try {
            this._router.verifyMessage(NetworkRouterDirection.Out, msg);

            if (this._router.checkClientRouting(NetworkRouterDirection.Out, msg, msgMeta)) {
                this._client.sendMessage(msg);
            }
        } catch (err) {
            this.routingError(String(err), { message: String(msg) });
        }
    }

    private handleReceivedMessage(entrypoint: MessageEntrypoint, msgName: string, data: string, payload: Payload): void {
        try {
            let msg = this.unpackMessage(msgName, data, payload);
            let msgMeta = this.createMessageMetaInformation(msg, entrypoint);

            logging.debug(`Received message: ${String(msg)}`, "network", { entrypoint: String(entrypoint) });

            if (this._router.checkLocalRouting(NetworkRouterDirection.In, msg, msgMeta)) {
                this._messageBus.dispatch(msg, msgMeta);
            }
        } catch (err) {
            this.routingError(String(err), { data: data });
        }
    }

    private unpackMessage(msgName: string, data: string, payload: Payload): Message {
        // Look up the actual message via its name
        let msgType = MessageTypesCatalog.findItem(msgName);
        if (!msgType) {
            throw new Error(`The message type '${msgName}' is unknown`);
        }

        let msg = Message.convertFromJSON(msgType, data);
        this._router.verifyMessage(NetworkRouterDirection.In, msg);

        msg.hops.push(this._compData.compID);
        msg.payload.decode(payload);

        return msg;
    }

    private createMessageMetaInformation(msg: Message, entrypoint: MessageEntrypoint, ...args: any[]): MessageMetaInformation {
        for (const [msgType, metaType] of Object.entries(this._metaInformationTypes)) {
            if (msg.messageCategory == msgType) {
                return new metaType(entrypoint, ...args) as MessageMetaInformation;
            }
        }

        throw new Error("No meta information type associated with message type");
    }

    private routingError(msg: string, params: Record<string, any>): void {
        logging.error(`A routing error occurred: ${msg}`, "network", params);
    }

    /**
     * The client instance.
     */
    public get client(): Client {
        return this._client;
    }
}
