import { CommandComposer } from "../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../core/messaging/composers/CommandReplyComposer";
import { MessageBuilder } from "../core/messaging/composers/MessageBuilder";
import { Command } from "../core/messaging/Command";
import { CommandReply } from "../core/messaging/CommandReply";
import { Message } from "../core/messaging/Message";

/**
 * A generic PING command. Requires a ``PingReply`` reply.
 */
@Message.define("command/general/ping")
export class PingCommand extends Command {
    public readonly payload: string = "PING";

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, chain: Message | null = null): CommandComposer<PingCommand> {
        return messageBuilder.buildCommand(PingCommand, {}, chain);
    }
}

/**
 * Reply to the ``PingCommand``.
 */
@Message.define("command/general/ping/reply")
export class PingReply extends CommandReply {
    public readonly payload: string = "PONG";

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, cmd: PingCommand, success: boolean = true, message: string = ""):
        CommandReplyComposer<PingReply> {
        return messageBuilder.buildCommandReply(PingReply, cmd, success, message);
    }
}
