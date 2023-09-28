import { Type } from "class-transformer";

import { Command } from "../core/messaging/Command";
import { CommandReply } from "../core/messaging/CommandReply";
import { CommandComposer } from "../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../core/messaging/composers/CommandReplyComposer";
import { MessageBuilder } from "../core/messaging/composers/MessageBuilder";
import { Message } from "../core/messaging/Message";
import { Project } from "../data/entities/Project";
import { PingCommand } from "./NetworkCommands";

/**
 * Command to fetch all projects of the current user. Requires a ``ListProjectsReply`` reply.
 */
@Message.define("command/project/list")
export class ListProjectsCommand extends Command {
    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, chain: Message | null = null): CommandComposer<ListProjectsCommand> {
        return messageBuilder.buildCommand(ListProjectsCommand, {}, chain);
    }
}

/**
 * Reply to ``ListProjectsCommand``.
 */
@Message.define("command/project/list/reply")
export class ListProjectsReply extends CommandReply {
    // @ts-ignore
    @Type(() => Project)
    public readonly projects: Project[] = [];

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, cmd: PingCommand, projects: Project[], success: boolean = true, message: string = ""):
        CommandReplyComposer<ListProjectsReply> {
        return messageBuilder.buildCommandReply(ListProjectsReply, cmd, success, message, { projects: projects });
    }
}
