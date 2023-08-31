import { UnitID } from "../../../utils/UnitID";
import { Command } from "../Command";
import { CommandReply } from "../CommandReply";
import { Event } from "../Event";
import { type ConstructableMessage, Message, type MessageCategory } from "../Message";
import { type MessageBusProtocol } from "../MessageBusProtocol";
import { CommandComposer } from "./CommandComposer";
import { CommandReplyComposer } from "./CommandReplyComposer";
import { EventComposer } from "./EventComposer";

/**
 * A helper class to easily build and emit new messages.
 *
 * This class stores a reference to the global message bus and offers methods to easily create new messages and send them through the bus.
 */
export class MessageBuilder {
    private readonly _originID: UnitID;
    private readonly _messageBus: MessageBusProtocol;

    private readonly _counters: Record<MessageCategory, number> = {};

    /**
     * @param originID - The component identifier of the origin of newly created messages.
     * @param messageBus - The global message bus to use.
     */
    public constructor(originID: UnitID, messageBus: MessageBusProtocol) {
        this._originID = originID;
        this._messageBus = messageBus;

        this._counters[Command.Category] = 0;
        this._counters[CommandReply.Category] = 0;
        this._counters[Event.Category] = 0;
    }

    /**
     * Builds a new command.
     *
     * @param cmdType - The command type (i.e., a subclass of ``Command``).
     * @param values - Additional message values.
     * @param chain - A message that acts as the *predecessor* of the new message. Used to keep the same trace for multiple messages.
     *
     * @returns - The newly created command.
     *
     * @throws - If an unknown value was provided in ``values`.
     */
    public buildCommand<MsgType extends Command>(cmdType: ConstructableMessage<MsgType>,
                                                 values: Record<string, any> = {}, chain: Message | null = null): CommandComposer<MsgType> {
        this._counters[Command.Category] += 1;

        return new CommandComposer(this._originID, this._messageBus, cmdType, values, chain);
    }

    /**
     * Builds a new command reply.
     *
     * @param replyType - The command reply type (i.e., a subclass of ``CommandReply``).
     * @param command - The ``Command`` this reply is based on.
     * @param success - Whether the command *succeeded* or not (how this is interpreted depends on the command).
     * @param message - Additional message to include in the reply.
     * @param values - Additional message values.
     *
     * @returns - The newly created command reply.
     *
     * @throws - If an unknown value was provided in ``values`.
     */
    public buildCommandReply<MsgType extends CommandReply>(replyType: ConstructableMessage<MsgType>,
                                                           command: Command, success: boolean = true, message: string = "",
                                                           values: Record<string, any> = {}): CommandReplyComposer<MsgType> {
        this._counters[CommandReply.Category] += 1;

        values.success = success;
        values.message = message;
        values.unique = command.unique;

        return new CommandReplyComposer(this._originID, this._messageBus, replyType, command, values);
    }

    /**
     * Builds a new event.
     *
     * @param eventType - The event type (i.e., a subclass of ``Event``).
     * @param values - Additional message values.
     * @param chain - A message that acts as the *predecessor* of the new message. Used to keep the same trace for multiple messages.
     *
     * @returns - The newly created event.
     *
     * @throws - If an unknown value was provided in ``values`.
     */
    public buildEvent<MsgType extends Event>(eventType: ConstructableMessage<MsgType>,
                                             values: Record<string, any> = {}, chain: Message | null = null): EventComposer<MsgType> {
        this._counters[Event.Category] += 1;

        return new EventComposer(this._originID, this._messageBus, eventType, values, chain);
    }

    /**
     * Gets how many messages of specific message types have been created.
     *
     * The message builder keeps track of how many messages of the three major types ``Command``, ``CommandReply`` and
     * ``Event`` have been created.
     *
     * @param counter - The message type to get the count of. Must be either ``Command``, ``CommandReply`` or ``Event``.
     *
     * @returns - The number of messages already built of the specified type.
     */
    public getMessageCount(counter: MessageCategory): number {
        return counter in this._counters ? this._counters[counter] : 0;
    }
}
