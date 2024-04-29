import { Type } from "class-transformer";

import { Command } from "../../core/messaging/Command";
import { CommandReply } from "../../core/messaging/CommandReply";
import { CommandComposer } from "../../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../../core/messaging/composers/CommandReplyComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Message } from "../../core/messaging/Message";
import { type ConnectorInstanceID } from "../../data/entities/connector/ConnectorInstance";
import { type ProjectID } from "../../data/entities/project/Project";
import { ProjectJob } from "../../data/entities/project/ProjectJob";

/**
 * Command to fetch all project jobs of the current user. Requires a ``ListJobsReply`` reply.
 */
@Message.define("command/project-job/list")
export class ListProjectJobsCommand extends Command {
    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, chain: Message | null = null): CommandComposer<ListProjectJobsCommand> {
        return messageBuilder.buildCommand(ListProjectJobsCommand, {}, chain);
    }
}

/**
 * Reply to ``ListProjectJobsCommand``.
 *
 * @param jobs - The project jobs list.
 */
@Message.define("command/project-job/list/reply")
export class ListProjectJobsReply extends CommandReply {
    // @ts-ignore
    @Type(() => ProjectJob)
    public readonly jobs: ProjectJob[] = [];

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: ListProjectJobsCommand,
        jobs: ProjectJob[],
        success: boolean = true,
        message: string = "",
    ): CommandReplyComposer<ListProjectJobsReply> {
        return messageBuilder.buildCommandReply(ListProjectJobsReply, cmd, success, message, { jobs: jobs });
    }
}

/**
 * Command to initiate a publishing job.
 *
 * @param project_id - The project ID.
 * @param connector_instance - The connector instance ID.
 */
@Message.define("command/project-job/initiate")
export class InitiateProjectJobCommand extends Command {
    public readonly project_id: ProjectID = 0;
    public readonly connector_instance: ConnectorInstanceID = "";

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        projectID: ProjectID,
        connectorInstance: ConnectorInstanceID,
        chain: Message | null = null,
    ): CommandComposer<InitiateProjectJobCommand> {
        return messageBuilder.buildCommand(InitiateProjectJobCommand, { project_id: projectID, connector_instance: connectorInstance }, chain);
    }
}

/**
 * Reply to ``InitiateJobCommand``.
 */
@Message.define("command/project-job/initiate/reply")
export class InitiateProjectJobReply extends CommandReply {
    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: InitiateProjectJobCommand,
        success: boolean = true,
        message: string = "",
    ): CommandReplyComposer<InitiateProjectJobReply> {
        return messageBuilder.buildCommandReply(InitiateProjectJobReply, cmd, success, message);
    }
}
