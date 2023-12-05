import { Type } from "class-transformer";

import { Command } from "../core/messaging/Command";
import { CommandReply } from "../core/messaging/CommandReply";
import { CommandComposer } from "../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../core/messaging/composers/CommandReplyComposer";
import { MessageBuilder } from "../core/messaging/composers/MessageBuilder";
import { Message } from "../core/messaging/Message";
import { type ProjectFeatureID, type ProjectID } from "../data/entities/EntityTypes";
import { Project } from "../data/entities/Project";

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
        message: string = ""
    ): CommandReplyComposer<ListProjectsReply> {
        return messageBuilder.buildCommandReply(ListProjectsReply, cmd, success, message, { projects: projects });
    }
}

/**
 * Command to create a project. Requires a ``CreateProjectReply`` reply.
 *
 * @param title - The title of the project.
 * @param description - An optional project description.
 * @param features_selection - List of enabled user-selectable features.
 */
@Message.define("command/project/create")
export class CreateProjectCommand extends Command {
    public readonly title: string = "";
    public readonly description: string = "";

    // @ts-ignore
    @Type(() => String)
    public readonly features_selection: ProjectFeatureID[] = [];

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        title: string,
        description: string,
        features_selection: ProjectFeatureID[],
        chain: Message | null = null
    ): CommandComposer<CreateProjectCommand> {
        return messageBuilder.buildCommand(CreateProjectCommand, { title: title, description: description, features_selection: features_selection }, chain);
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
        message: string = ""
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
 * @param features_selection - List of enabled user-selectable features.
 */
@Message.define("command/project/update")
export class UpdateProjectCommand extends Command {
    public readonly project_id: ProjectID = 0;

    public readonly title: string = "";
    public readonly description: string = "";

    // @ts-ignore
    @Type(() => String)
    public readonly features_selection: ProjectFeatureID[] = [];

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        project_id: ProjectID,
        title: string,
        description: string,
        features_selection: ProjectFeatureID[],
        chain: Message | null = null
    ): CommandComposer<UpdateProjectCommand> {
        return messageBuilder.buildCommand(UpdateProjectCommand, {
            project_id: project_id, title: title, description: description, features_selection: features_selection
        }, chain);
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
        message: string = ""
    ): CommandReplyComposer<UpdateProjectReply> {
        return messageBuilder.buildCommandReply(UpdateProjectReply, cmd, success, message, { project_id: project_id });
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
        message: string = ""
    ): CommandReplyComposer<DeleteProjectReply> {
        return messageBuilder.buildCommandReply(DeleteProjectReply, cmd, success, message, { project_id: cmd.project_id });
    }
}
