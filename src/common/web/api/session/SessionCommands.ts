import { Command } from "../../core/messaging/Command";
import { CommandReply } from "../../core/messaging/CommandReply";
import { CommandComposer } from "../../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../../core/messaging/composers/CommandReplyComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Message } from "../../core/messaging/Message";

/**
 * Command to get a session value stored on the server. Requires a ``GetSessionValueReply`` reply.
 *
 * @param key - The value key.
 */
@Message.define("command/session/value/get")
export class GetSessionValueCommand extends Command {
    public readonly key: string = "";

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, key: string, chain: Message | null = null): CommandComposer<GetSessionValueCommand> {
        return messageBuilder.buildCommand(GetSessionValueCommand, { key: key }, chain);
    }
}

/**
 * Reply to ``GetSessionValueCommand``.
 *
 * @param value - The value or *undefined* if no such value was found.*/
@Message.define("command/session/value/get/reply")
export class GetSessionValueReply extends CommandReply {
    public readonly value: any = undefined;

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: GetSessionValueCommand,
        value: any,
        success: boolean = true,
        message: string = ""
    ): CommandReplyComposer<GetSessionValueReply> {
        return messageBuilder.buildCommandReply(GetSessionValueReply, cmd, success, message, { value: value });
    }
}

/**
 * Command to store a session value on the server. Requires a ``SetSessionValueReply`` reply.
 *
 * @param key - The value key.
 * @param value - The value to store.
 */
@Message.define("command/session/value/set")
export class SetSessionValueCommand extends Command {
    public readonly key: string = "";
    public readonly value: any = undefined;

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, key: string, value: any, chain: Message | null = null): CommandComposer<SetSessionValueCommand> {
        return messageBuilder.buildCommand(SetSessionValueCommand, { key: key, value: value }, chain);
    }
}

/**
 * Reply to ``SetSessionValueCommand``.
 *
 * @param settings - The new user settings (note that these might have been adjusted by the server).
 */
@Message.define("command/session/value/set/reply")
export class SetSessionValueReply extends CommandReply {
    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: SetSessionValueCommand,
        success: boolean = true,
        message: string = ""
    ): CommandReplyComposer<SetSessionValueReply> {
        return messageBuilder.buildCommandReply(SetSessionValueReply, cmd, success, message);
    }
}
