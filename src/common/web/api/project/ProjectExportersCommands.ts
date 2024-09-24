import { Type } from "class-transformer";

import { Command } from "../../core/messaging/Command";
import { CommandReply } from "../../core/messaging/CommandReply";
import { CommandComposer } from "../../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../../core/messaging/composers/CommandReplyComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Message } from "../../core/messaging/Message";
import { ProjectExporterDescriptor } from "../../data/exporters/ProjectExporterDescriptor";

/**
 * Command to fetch all project exporters. Requires a ``ListProjectExportersReply`` reply.
 */
@Message.define("command/project/export/list")
export class ListProjectExportersCommand extends Command {
    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, chain: Message | null = null): CommandComposer<ListProjectExportersCommand> {
        return messageBuilder.buildCommand(ListProjectExportersCommand, {}, chain);
    }
}

/**
 * Reply to ``Reply to ``ListProjectsCommand``.``.
 *
 * @param exporters - List of all project exporters.
 */
@Message.define("command/project/export/list/reply")
export class ListProjectExportersReply extends CommandReply {
    // @ts-ignore
    @Type(() => ProjectExporterDescriptor)
    public readonly exporters: ProjectExporterDescriptor[] = [];

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: ListProjectExportersCommand,
        exporters: ProjectExporterDescriptor[],
        success: boolean = true,
        message: string = ""
    ): CommandReplyComposer<ListProjectExportersReply> {
        return messageBuilder.buildCommandReply(ListProjectExportersReply, cmd, success, message, { exporters: exporters });
    }
}
