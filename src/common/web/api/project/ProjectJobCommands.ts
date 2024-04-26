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
@Message.define("command/job/list")
export class ListJobsCommand extends Command {
    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, chain: Message | null = null): CommandComposer<ListJobsCommand> {
        return messageBuilder.buildCommand(ListJobsCommand, {}, chain);
    }
}

/**
 * Reply to ``ListJobsCommand``.
 *
 * @param project_jobs - The project jobs list.
 */
@Message.define("command/job/list/reply")
export class ListJobsReply extends CommandReply {
    // @ts-ignore
    @Type(() => ProjectJob)
    public readonly project_jobs: ProjectJob[] = [];

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: ListJobsCommand,
        projectJobs: ProjectJob[],
        success: boolean = true,
        message: string = "",
    ): CommandReplyComposer<ListJobsReply> {
        return messageBuilder.buildCommandReply(ListJobsReply, cmd, success, message, { project_jobs: projectJobs });
    }
}

/**
 * Command to initiate a publishing job.
 *
 * @param project_id - The project ID.
 * @param connector_instance - The connector instance ID.
 */
@Message.define("command/job/initiate")
export class InitiateJobCommand extends Command {
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
    ): CommandComposer<InitiateJobCommand> {
        return messageBuilder.buildCommand(InitiateJobCommand, { project_id: projectID, connector_instance: connectorInstance }, chain);
    }
}

/**
 * Reply to ``InitiateJobCommand``.
 */
@Message.define("command/job/initiate/reply")
export class InitiateJobReply extends CommandReply {
    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: InitiateJobCommand,
        success: boolean = true,
        message: string = "",
    ): CommandReplyComposer<InitiateJobReply> {
        return messageBuilder.buildCommandReply(InitiateJobReply, cmd, success, message);
    }
}
