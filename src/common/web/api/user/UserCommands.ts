import { Type } from "class-transformer";

import { Command } from "../../core/messaging/Command";
import { CommandReply } from "../../core/messaging/CommandReply";
import { CommandComposer } from "../../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../../core/messaging/composers/CommandReplyComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Message } from "../../core/messaging/Message";
import { UserSettings } from "../../data/entities/user/UserSettings";

/**
 * Command to get the settings of the current user. Requires a ``GetUserSettingsReply`` reply.
 */
@Message.define("command/user/settings/get")
export class GetUserSettingsCommand extends Command {
    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, chain: Message | null = null): CommandComposer<GetUserSettingsCommand> {
        return messageBuilder.buildCommand(GetUserSettingsCommand, {}, chain);
    }
}

/**
 * Reply to ``GetUserSettingsCommand``.
 *
 * @param settings - The user settings.
 */
@Message.define("command/user/settings/get/reply")
export class GetUserSettingsReply extends CommandReply {
    // @ts-ignore
    @Type(() => UserSettings)
    public readonly settings: UserSettings = new UserSettings();

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: GetUserSettingsCommand,
        settings: UserSettings,
        success: boolean = true,
        message: string = ""
    ): CommandReplyComposer<GetUserSettingsReply> {
        return messageBuilder.buildCommandReply(GetUserSettingsReply, cmd, success, message, { settings: settings });
    }
}

/**
 * Command to set the settings of the current user. Requires a ``SetUserSettingsReply`` reply.
 *
 * @param settings - The new user settings.
 */
@Message.define("command/user/settings/set")
export class SetUserSettingsCommand extends Command {
    // @ts-ignore
    @Type(() => UserSettings)
    public readonly settings: UserSettings = new UserSettings();

    /**
     * Helper function to easily build this message.
     */
    public static build(messageBuilder: MessageBuilder, settings: UserSettings, chain: Message | null = null): CommandComposer<SetUserSettingsCommand> {
        return messageBuilder.buildCommand(SetUserSettingsCommand, { settings: settings }, chain);
    }
}

/**
 * Reply to ``SetUserSettingsCommand``.
 */
@Message.define("command/user/settings/set/reply")
export class SetUserSettingsReply extends CommandReply {
    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: SetUserSettingsCommand,
        success: boolean = true,
        message: string = ""
    ): CommandReplyComposer<SetUserSettingsReply> {
        return messageBuilder.buildCommandReply(SetUserSettingsReply, cmd, success, message);
    }
}
