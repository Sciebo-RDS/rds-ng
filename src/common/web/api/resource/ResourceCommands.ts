import { Type } from "class-transformer";

import { Command } from "../../core/messaging/Command";
import { CommandReply } from "../../core/messaging/CommandReply";
import { CommandComposer } from "../../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../../core/messaging/composers/CommandReplyComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Message } from "../../core/messaging/Message";
import { Resource, ResourceType } from "../../data/entities/resource/Resource";
import { ResourcesList } from "../../data/entities/resource/ResourcesList";

/**
 * Command to assign a broker to access the user's resources. Requires a ``AssignResourcesBrokerReply`` reply.
 *
 * @param broker - The broker to use.
 * @param config - The broker configuration.
 */
@Message.define("command/resource/assign-broker")
export class AssignResourcesBrokerCommand extends Command {
    public readonly broker: string = "";
    public readonly config: any = null;

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        broker: string,
        config: any,
        chain: Message | null = null,
    ): CommandComposer<AssignResourcesBrokerCommand> {
        return messageBuilder.buildCommand(AssignResourcesBrokerCommand, { broker: broker, config: config }, chain);
    }
}

/**
 * Reply to ``AssignResourcesBrokerCommand``.
 */
@Message.define("command/resource/assign-broker/reply")
export class AssignResourcesBrokerReply extends CommandReply {
    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: AssignResourcesBrokerCommand,
        success: boolean = true,
        message: string = "",
    ): CommandReplyComposer<AssignResourcesBrokerReply> {
        return messageBuilder.buildCommandReply(AssignResourcesBrokerReply, cmd, success, message);
    }
}

/**
 * Command to fetch all available resources.
 *
 * @param root - The root path (or empty if the system root should be used).
 * @param include_folders - Whether to list folders (if this is set to false, no recursion will occur independent of `recursive`).
 * @param include_files - Whether to list files.
 * @param recursive - Whether to recursively process all sub-folders as well.
 */
@Message.define("command/resource/list")
export class ListResourcesCommand extends Command {
    public readonly root: string = "";

    public readonly include_folders: boolean = true;
    public readonly include_files: boolean = true;

    public readonly recursive: boolean = true;

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        root: string = "",
        includeFolders: boolean = true,
        includeFiles: boolean = true,
        recursive: boolean = true,
        chain: Message | null = null,
    ): CommandComposer<ListResourcesCommand> {
        return messageBuilder.buildCommand(
            ListResourcesCommand,
            { root: root, include_folders: includeFolders, include_files: includeFiles, recursive: recursive },
            chain,
        );
    }
}

/**
 * Reply to ``ListResourcesCommand``.
 *
 * @param resources - List of all resources.
 */
@Message.define("command/resource/list/reply")
export class ListResourcesReply extends CommandReply {
    // @ts-ignore
    @Type(() => ResourcesList)
    public readonly resources: ResourcesList = new ResourcesList(new Resource("", "", ResourceType.Folder));

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: ListResourcesCommand,
        resources: ResourcesList,
        success: boolean = true,
        message: string = "",
    ): CommandReplyComposer<ListResourcesReply> {
        return messageBuilder.buildCommandReply(ListResourcesReply, cmd, success, message, { resources: resources });
    }
}
