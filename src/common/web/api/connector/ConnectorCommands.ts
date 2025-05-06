import { Type } from "class-transformer";

import { Command } from "../../core/messaging/Command";
import { CommandReply } from "../../core/messaging/CommandReply";
import { CommandComposer } from "../../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../../core/messaging/composers/CommandReplyComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Message } from "../../core/messaging/Message";
import { Connector } from "../../data/entities/connector/Connector";

/**
 * Command to fetch all available connectors.
 */
@Message.define("command/connector/list")
export class ListConnectorsCommand extends Command {
    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, chain: Message | null = null): CommandComposer<ListConnectorsCommand> {
        return messageBuilder.buildCommand(ListConnectorsCommand, {}, chain);
    }
}

/**
 * Reply to ``ListConnectorsCommand``.
 *
 * @param connectors - List of all connectors.
 */
@Message.define("command/connector/list/reply")
export class ListConnectorsReply extends CommandReply {
    // @ts-ignore
    @Type(() => Connector)
    public readonly connectors: Connector[] = [];

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: ListConnectorsCommand,
        connectors: Connector[],
        success: boolean = true,
        message: string = ""
    ): CommandReplyComposer<ListConnectorsReply> {
        return messageBuilder.buildCommandReply(ListConnectorsReply, cmd, success, message, { connectors: connectors });
    }
}
