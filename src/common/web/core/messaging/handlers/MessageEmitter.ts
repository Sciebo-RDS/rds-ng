import { UnitID } from "../../../utils/UnitID";
import { Command } from "../Command";
import { type CommandDoneCallback, type CommandFailCallback, CommandReply } from "../CommandReply";
import { Event } from "../Event";
import { Message } from "../Message";
import { Channel } from "../Channel";
import logging from "../../logging/Logging";
import { MessageEntrypoint, MessageMetaInformation } from "../meta/MessageMetaInformation";
import { type Constructable } from "../../../utils/Types";
import { CommandMetaInformation } from "../meta/CommandMetaInformation";
import { CommandReplyMetaInformation } from "../meta/CommandReplyMetaInformation";
import { EventMetaInformation } from "../meta/EventMetaInformation";

export type MessageValues = Record<string, any>;

export enum MessageEmitterCounter {
    Command = "command",
    CommandReply = "commandreply",
    Event = "event"
}

/**
 * A helper class to easily create and emit messages.
 *
 * This class stores a reference to the global message bus and offers methods to easily create new messages and send them through the bus.
 */
export class MessageEmitter {
    private readonly _originID: UnitID;
    private readonly _counters: Record<string, number> = {};

    // TODO: MsgBus

    /**
     * @param originID - The component identifier of the origin of newly created messages.
     */
    public constructor(originID: UnitID) {
        this._originID = originID;

        this._counters[MessageEmitterCounter.Command] = 0;
        this._counters[MessageEmitterCounter.CommandReply] = 0;
        this._counters[MessageEmitterCounter.Event] = 0;
    }

    /**
     * Emits a new command.
     *
     * @param cmdType - The command type (i.e., a subclass of ``Command``).
     * @param target - The destination of the message.
     * @param values - Additional message values.
     * @param doneCallback - Callback when a reply for the command was received.
     * @param failCallback - Callback when no reply for the command was received.
     * @param timeout - The timeout (in seconds) until a command is deemed *not answered*. Pass ``0`` to disable timeouts.
     * @param chain - A message that acts as the *predecessor* of the new message. Used to keep the same trace for multiple messages.
     *
     * @returns - The newly created command.
     *
     * @throws - If an unknown value was provided in ``values`.
     */
    public emitCommand<T extends Command>(cmdType: Constructable<T>, target: Channel, values: MessageValues,
                                          doneCallback: CommandDoneCallback | undefined = undefined,
                                          failCallback: CommandFailCallback | undefined = undefined,
                                          timeout: number = 0.0,
                                          chain: Message | null = null): T {
        if (timeout > 0.0 && failCallback == undefined) {
            logging.info(`Sending a command (${cmdType}) with a timeout but no fail callback`, "bus");
        }

        this._counters[MessageEmitterCounter.Command] += 1;

        let meta = new CommandMetaInformation(MessageEntrypoint.Local, doneCallback, failCallback, timeout);
        return this.emit(cmdType, meta, this._originID, target, [], chain, values);
    }

    /**
     * Emits a new command reply.
     *
     * Most parameters, like the proper target, are extracted from the originating command.
     *
     * @param replyType - The command reply type (i.e., a subclass of ``CommandReply``).
     * @param command - The ``Command`` this reply is based on.
     * @param values - Additional message values.
     * @param success - Whether the command *succeeded* or not (how this is interpreted depends on the command).
     * @param message - Additional message to include in the reply.
     *
     * @returns - The newly created command reply.
     *
     * @throws - If an unknown value was provided in ``values`.
     */
    public emitReply<T extends CommandReply>(replyType: Constructable<T>, command: Command, values: MessageValues,
                                             success: boolean = true, message: string = ""): T {
        this._counters[MessageEmitterCounter.CommandReply] += 1;

        values.success = success;
        values.message = message;
        values.unique = command.unique;

        let meta = new CommandReplyMetaInformation(MessageEntrypoint.Local);
        return this.emit(replyType, meta, this._originID, Channel.direct(command.origin.toString()), [], command, values);
    }

    /**
     * Emits a new event.
     *
     * @param eventType - The event type (i.e., a subclass of ``Event``).
     * @param target - The destination of the message.
     * @param values - Additional message values.
     * @param chain - A message that acts as the *predecessor* of the new message. Used to keep the same trace for multiple messages.
     *
     * @returns - The newly created event.
     *
     * @throws - If an unknown value was provided in ``values`.
     */
    public emitEvent<T extends Event>(eventType: Constructable<T>, target: Channel, values: MessageValues, chain: Message | null = null): T {
        this._counters[MessageEmitterCounter.Event] += 1;

        let meta = new EventMetaInformation(MessageEntrypoint.Local);
        return this.emit(eventType, meta, this._originID, target, [], chain, values);
    }

    public getMessageCount(counter: MessageEmitterCounter): number {
        return counter in this._counters ? this._counters[counter] : 0;
    }

    private emit<T extends Message>(msgCtor: Constructable<T>, msgMeta: MessageMetaInformation,
                                    origin: UnitID, target: Channel, prevHops: UnitID[], chain: Message | null, values: MessageValues): T {
        let msg = this.createMessage<T>(msgCtor, origin, target, prevHops, chain, values);
        // TODO
        // this._messageBus.dispatch(msg, msgMeta);
        return msg;
    }

    private createMessage<T extends Message>(msgCtor: Constructable<T>, origin: UnitID, target: Channel, prevHops: UnitID[], chain: Message | null,
                                             values: MessageValues): T {
        let msg = chain != null ?
            new msgCtor(origin, this._originID, target, [...prevHops, this._originID], chain.trace) as T :
            new msgCtor(origin, this._originID, target, [...prevHops, this._originID]) as T;

        for (const [key, value] of Object.entries(values)) {
            if (key in msg) {
                msg[key as keyof T] = value;
            } else {
                throw new Error(`Provided unknown value '${key}' for message type ${msg.name}`);
            }
        }

        return msg;
    }
}
