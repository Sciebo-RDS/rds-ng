import { Type } from "class-transformer";

import { Command } from "../../core/messaging/Command";
import { CommandReply } from "../../core/messaging/CommandReply";
import { CommandComposer } from "../../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../../core/messaging/composers/CommandReplyComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Message } from "../../core/messaging/Message";
import { MetadataProfileContainer, type MetadataProfileContainerList } from "../../data/entities/metadata/MetadataProfileContainer";

/**
 * Command to fetch all global metadata profiles. Requires a ``GetMetadataProfilesReply`` reply.
 */
@Message.define("command/metadata/profiles")
export class GetMetadataProfilesCommand extends Command {
    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, chain: Message | null = null): CommandComposer<GetMetadataProfilesCommand> {
        return messageBuilder.buildCommand(GetMetadataProfilesCommand, {}, chain);
    }
}

/**
 * Reply to ``GetMetadataProfilesCommand``.
 *
 * @param profiles - List of all global profiles.
 */
@Message.define("command/metadata/profiles/reply")
export class GetMetadataProfilesReply extends CommandReply {
    // @ts-ignore
    @Type(() => MetadataProfileContainer)
    public readonly profiles: MetadataProfileContainerList = [];

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: GetMetadataProfilesCommand,
        profiles: MetadataProfileContainerList,
        success: boolean = true,
        message: string = ""
    ): CommandReplyComposer<GetMetadataProfilesReply> {
        return messageBuilder.buildCommandReply(GetMetadataProfilesReply, cmd, success, message, { profiles: profiles });
    }
}
