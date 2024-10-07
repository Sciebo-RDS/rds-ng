import { Type } from "class-transformer";

import { Command } from "../../core/messaging/Command";
import { CommandReply } from "../../core/messaging/CommandReply";
import { CommandComposer } from "../../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../../core/messaging/composers/CommandReplyComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Message } from "../../core/messaging/Message";
import { type ProjectFeatureID } from "../../data/entities/project/features/ProjectFeature";
import { type ProjectID } from "../../data/entities/project/Project";
import { ProjectExporterDescriptor, type ProjectExporterID } from "../../data/exporters/ProjectExporterDescriptor";

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

/**
 * Command to export a project. Requires an ``ExportProjectReply`` reply.
 */
@Message.define("command/project/export")
export class ExportProjectCommand extends Command {
    public readonly project_id: ProjectID = 0;

    public readonly exporter: ProjectExporterID = "";
    public readonly scope: ProjectFeatureID = "";

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        projectID: ProjectID,
        exporter: ProjectExporterID,
        scope: ProjectFeatureID,
        chain: Message | null = null
    ): CommandComposer<ExportProjectCommand> {
        return messageBuilder.buildCommand(ExportProjectCommand, { project_id: projectID, exporter: exporter, scope: scope }, chain);
    }
}

/**
 * Reply to ``ExportProjectCommand``.
 *
 * @param mimetype - The MIME type of the export result.
 */
@Message.define("command/project/export/reply")
export class ExportProjectReply extends CommandReply {
    public readonly mimetype: string = "";

    /**
     * The data of the export result.
     */
    public get data(): ArrayBuffer | undefined {
        if (this.payload.contains("data")) {
            return this.payload.get("data") as ArrayBuffer;
        }
        return undefined;
    }

    /**
     * Sets the data of the export result.
     *
     * @param data - The export result data.
     */
    public set data(data: ArrayBuffer) {
        this.payload.set("data", data);
    }

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: ExportProjectCommand,
        mimetype: string,
        data: ArrayBuffer,
        success: boolean = true,
        message: string = ""
    ): CommandReplyComposer<ExportProjectReply> {
        const composer = messageBuilder.buildCommandReply(ExportProjectReply, cmd, success, message, { mimetype: mimetype });
        composer.addPayload("data", data);
        return composer;
    }
}
