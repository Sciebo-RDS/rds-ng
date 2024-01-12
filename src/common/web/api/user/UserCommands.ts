import { Type } from "class-transformer";

import { Command } from "../../core/messaging/Command";
import { CommandReply } from "../../core/messaging/CommandReply";
import { CommandComposer } from "../../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../../core/messaging/composers/CommandReplyComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Message } from "../../core/messaging/Message";
import { UserConfiguration } from "../../data/entities/user/UserConfiguration";

/**
 * Command to get the configuration of the current user. Requires a ``GetUserConfigurationReply`` reply.
 */
@Message.define("command/user/configuration/get")
export class GetUserConfigurationCommand extends Command {
    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, chain: Message | null = null): CommandComposer<GetUserConfigurationCommand> {
        return messageBuilder.buildCommand(GetUserConfigurationCommand, {}, chain);
    }
}

/**
 * Reply to ``GetUserConfigurationCommand``.
 *
 * @param configuration - The user configuration.
 */
@Message.define("command/user/configuration/get/reply")
export class GetUserConfigurationReply extends CommandReply {
    // @ts-ignore
    @Type(() => UserConfiguration)
    public readonly configuration: UserConfiguration = new UserConfiguration();

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: GetUserConfigurationCommand,
        configuration: UserConfiguration,
        success: boolean = true,
        message: string = ""
    ): CommandReplyComposer<GetUserConfigurationReply> {
        return messageBuilder.buildCommandReply(GetUserConfigurationReply, cmd, success, message, { configuration: configuration });
    }
}

/**
 * Command to set the configuration of the current user. Requires a ``SetUserConfigurationReply`` reply.
 *
 * @param configuration - The new user configuration.
 */
@Message.define("command/user/configuration/set")
export class SetUserConfigurationCommand extends Command {
    // @ts-ignore
    @Type(() => UserConfiguration)
    public readonly configuration: UserConfiguration = new UserConfiguration();

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, configuration: UserConfiguration, chain: Message | null = null): CommandComposer<SetUserConfigurationCommand> {
        return messageBuilder.buildCommand(SetUserConfigurationCommand, { configuration: configuration }, chain);
    }
}

/**
 * Reply to ``SetUserConfigurationCommand``.
 */
@Message.define("command/user/configuration/set/reply")
export class SetUserConfigurationReply extends CommandReply {
    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: SetUserConfigurationCommand,
        success: boolean = true,
        message: string = ""
    ): CommandReplyComposer<SetUserConfigurationReply> {
        return messageBuilder.buildCommandReply(SetUserConfigurationReply, cmd, success, message);
    }
}
