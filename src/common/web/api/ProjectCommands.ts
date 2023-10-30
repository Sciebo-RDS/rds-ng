import { Type } from "class-transformer";

import { Command } from "../core/messaging/Command";
import { CommandReply } from "../core/messaging/CommandReply";
import { CommandComposer } from "../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../core/messaging/composers/CommandReplyComposer";
import { MessageBuilder } from "../core/messaging/composers/MessageBuilder";
import { Message } from "../core/messaging/Message";
import { Project, type ProjectID } from "../data/entities/Project";

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
    public static build(messageBuilder: MessageBuilder, cmd: ListProjectsCommand, projects: Project[], success: boolean = true, message: string = ""):
        CommandReplyComposer<ListProjectsReply> {
        return messageBuilder.buildCommandReply(ListProjectsReply, cmd, success, message, { projects: projects });
    }
}

/**
 * Command to delete a project of the current user. Requires a ``DeleteProjectReply`` reply.
 *
 * @param project_id - The ID of the project to delete.
 */
@Message.define("command/project/delete")
export class DeleteProjectCommand extends Command {
    public readonly project_id: ProjectID = 0;

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, projectID: ProjectID, chain: Message | null = null): CommandComposer<ListProjectsCommand> {
        return messageBuilder.buildCommand(DeleteProjectCommand, { project_id: projectID }, chain);
    }
}


/**
 * Reply to ``DeleteProjectCommand``.
 */
@Message.define("command/project/delete/reply")
export class DeleteProjectReply extends CommandReply {
    public readonly project_id: ProjectID = 0;

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, cmd: DeleteProjectCommand, success: boolean = true, message: string = ""):
        CommandReplyComposer<ListProjectsReply> {
        return messageBuilder.buildCommandReply(DeleteProjectReply, cmd, success, message, { project_id: cmd.project_id });
    }
}
