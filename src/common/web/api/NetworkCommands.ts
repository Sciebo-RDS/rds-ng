import { Channel } from "../core/messaging/Channel";
import { Command } from "../core/messaging/Command";
import { type CommandDoneCallback, type CommandFailCallback, CommandReply } from "../core/messaging/CommandReply";
import { MessageEmitter } from "../core/messaging/handlers/MessageEmitter";
import { Message } from "../core/messaging/Message";

/**
 * A generic PING command. Requires a ``PingReply`` reply.
 */
@Message.define("command/general/ping")
export class PingCommand extends Command {
    public readonly payload: string = "PING";

    /**
     * Helper function to easily emit this message.
     */
    public static emit(messageEmitter: MessageEmitter, target: Channel,
                       doneCallback: CommandDoneCallback | null = null,
                       failCallback: CommandFailCallback | null = null,
                       timeout: number = 0.0,
                       chain: Message | null = null): void {
        messageEmitter.emitCommand(PingCommand, target, {}, doneCallback, failCallback, timeout, chain);
    }
}

/**
 * Reply to the ``PingCommand``.
 */
@Message.define("command/general/ping/reply")
export class PingReply extends CommandReply {
    public readonly payload: string = "PONG";

    /**
     * Helper function to easily emit this message.
     */
    public static emit(messageEmitter: MessageEmitter, cmd: PingCommand, success: boolean = true, message: string = ""): void {
        messageEmitter.emitReply(PingReply, cmd, {}, success, message);
    }
}
