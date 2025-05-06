import { Type } from "class-transformer";

import { Command } from "../../core/messaging/Command";
import { CommandReply } from "../../core/messaging/CommandReply";
import { CommandComposer } from "../../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../../core/messaging/composers/CommandReplyComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Message } from "../../core/messaging/Message";
import { type RecordID } from "../../data/entities/project/logbook/ProjectLogbookRecord";
import { ProjectLogbookType } from "../../data/entities/project/logbook/ProjectLogbookType";
import { Project, type ProjectID } from "../../data/entities/project/Project";
import { ProjectOptions } from "../../data/entities/project/ProjectOptions";

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
 *
 * @param projects - The projects list.
 */
@Message.define("command/project/list/reply")
export class ListProjectsReply extends CommandReply {
    // @ts-ignore
    @Type(() => Project)
    public readonly projects: Project[] = [];

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: ListProjectsCommand,
        projects: Project[],
        success: boolean = true,
        message: string = "",
    ): CommandReplyComposer<ListProjectsReply> {
        return messageBuilder.buildCommandReply(ListProjectsReply, cmd, success, message, { projects: projects });
    }
}

/**
 * Command to create a project. Requires a ``CreateProjectReply`` reply.
 *
 * @param resources_path - The resources path of the project.
 * @param title - The title of the project.
 * @param description - An optional project description.
 * @param options - The project options.
 */
@Message.define("command/project/create")
export class CreateProjectCommand extends Command {
    public readonly resources_path: string = "";

    public readonly title: string = "";
    public readonly description: string = "";

    // @ts-ignore
    @Type(() => ProjectOptions)
    public readonly options: ProjectOptions = new ProjectOptions();

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        resourcesPath: string,
        title: string,
        description: string,
        options: ProjectOptions,
        chain: Message | null = null,
    ): CommandComposer<CreateProjectCommand> {
        return messageBuilder.buildCommand(
            CreateProjectCommand,
            { resources_path: resourcesPath, title: title, description: description, options: options },
            chain,
        );
    }
}

/**
 * Reply to ``CreateProjectCommand``.
 *
 * @param project_id: The ID of the created project.
 */
@Message.define("command/project/create/reply")
export class CreateProjectReply extends CommandReply {
    public readonly project_id: ProjectID = 0;

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: CreateProjectCommand,
        project_id: ProjectID,
        success: boolean = true,
        message: string = "",
    ): CommandReplyComposer<CreateProjectReply> {
        return messageBuilder.buildCommandReply(CreateProjectReply, cmd, success, message, { project_id: project_id });
    }
}

/**
 * Command to update a project. Requires an ``UpdateProjectReply`` reply.
 * Note that the project features are updated using a separate ``UpdateProjectFeaturesCommand`` message.
 *
 * @param project_id - The ID of the project to update.
 * @param title - The title of the project.
 * @param description - An optional project description.
 * @param options - The project options.
 */
@Message.define("command/project/update")
export class UpdateProjectCommand extends Command {
    public readonly project_id: ProjectID = 0;

    public readonly title: string = "";
    public readonly description: string = "";

    // @ts-ignore
    @Type(() => ProjectOptions)
    public readonly options: ProjectOptions = new ProjectOptions();

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        project_id: ProjectID,
        title: string,
        description: string,
        options: ProjectOptions,
        chain: Message | null = null,
    ): CommandComposer<UpdateProjectCommand> {
        return messageBuilder.buildCommand(UpdateProjectCommand, { project_id: project_id, title: title, description: description, options: options }, chain);
    }
}

/**
 * Reply to ``UpdateProjectCommand``.
 *
 * @param project_id - The ID of the updated project.
 */
@Message.define("command/project/update/reply")
export class UpdateProjectReply extends CommandReply {
    public readonly project_id: ProjectID = 0;

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: UpdateProjectCommand,
        project_id: ProjectID,
        success: boolean = true,
        message: string = "",
    ): CommandReplyComposer<UpdateProjectReply> {
        return messageBuilder.buildCommandReply(UpdateProjectReply, cmd, success, message, { project_id: project_id });
    }
}

/**
 * Marks a project logbook entry as seen. Requires an ``ProjectLogbookMarkSeenReply`` reply.
 *
 * @param logbook_type - The logbook type to mark.
 * @param project_id - The ID of the project containing the logbook.
 * @param record - The record ID.
 * @param mark_all - If true, all records will be marked as seen (ignores project and record IDs).
 */
@Message.define("command/project/logbook/mark-seen")
export class MarkProjectLogbookSeenCommand extends Command {
    public readonly logbook_type: ProjectLogbookType = ProjectLogbookType.JobHistory;

    public readonly project_id: ProjectID = 0;
    public readonly record: RecordID = 0;

    public readonly mark_all: boolean = false;

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        logbookType: ProjectLogbookType,
        projectID: ProjectID,
        record: RecordID,
        markAll: boolean = false,
        chain: Message | null = null,
    ): CommandComposer<MarkProjectLogbookSeenCommand> {
        return messageBuilder.buildCommand(
            MarkProjectLogbookSeenCommand,
            { logbook_type: logbookType, project_id: projectID, record: record, mark_all: markAll },
            chain,
        );
    }
}

/**
 * Reply to ``ProjectLogbookMarkSeenCommand``.
 */
@Message.define("command/project/logbook/mark-seen/reply")
export class MarkProjectLogbookSeenReply extends CommandReply {
    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: MarkProjectLogbookSeenCommand,
        success: boolean = true,
        message: string = "",
    ): CommandReplyComposer<MarkProjectLogbookSeenReply> {
        return messageBuilder.buildCommandReply(MarkProjectLogbookSeenReply, cmd, success, message);
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
    public static build(messageBuilder: MessageBuilder, projectID: ProjectID, chain: Message | null = null): CommandComposer<DeleteProjectCommand> {
        return messageBuilder.buildCommand(DeleteProjectCommand, { project_id: projectID }, chain);
    }
}

/**
 * Reply to ``DeleteProjectCommand``.
 *
 * @param project_id - The ID of the deleted project.
 */
@Message.define("command/project/delete/reply")
export class DeleteProjectReply extends CommandReply {
    public readonly project_id: ProjectID = 0;

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: DeleteProjectCommand,
        success: boolean = true,
        message: string = "",
    ): CommandReplyComposer<DeleteProjectReply> {
        return messageBuilder.buildCommandReply(DeleteProjectReply, cmd, success, message, { project_id: cmd.project_id });
    }
}
