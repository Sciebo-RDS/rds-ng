import { Command } from "../core/messaging/Command";
import { CommandReply } from "../core/messaging/CommandReply";
import { Message } from "../core/messaging/Message";

/**
 * A generic PING command. Requires a ``PingReply`` reply.
 */
@Message.define("command/general/ping")
export class PingCommand extends Command {
    public readonly payload: string = "PING";
}

/**
 * Reply to the ``PingCommand``.
 */
@Message.define("command/general/ping/reply")
export class PingReply extends CommandReply {
    public readonly payload: string = "PONG";
}
