import { Command } from "../../core/messaging/Command";
import { CommandReply } from "../../core/messaging/CommandReply";
import { CommandComposer } from "../../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../../core/messaging/composers/CommandReplyComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Message } from "../../core/messaging/Message";

/**
 * Command to perform an authorization request. Requires a ``RequestAuthorizationReply`` reply.
 */
@Message.define("command/authorization/request")
export class RequestAuthorizationCommand extends Command {
    public readonly auth_id: string = "";

    public readonly strategy: string = "";
    public readonly data: any = null;

    public readonly fingerprint: string = "";

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        authID: string,
        strategy: string,
        data: any,
        fingerprint: string,
        chain: Message | null = null,
    ): CommandComposer<RequestAuthorizationCommand> {
        return messageBuilder.buildCommand(RequestAuthorizationCommand, { auth_id: authID, strategy: strategy, data: data, fingerprint: fingerprint }, chain);
    }
}

/**
 * Reply to ``RequestAuthorizationCommand``.
 */
@Message.define("command/authorization/request/reply")
export class RequestAuthorizationReply extends CommandReply {
    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: RequestAuthorizationCommand,
        success: boolean = true,
        message: string = "",
    ): CommandReplyComposer<RequestAuthorizationReply> {
        return messageBuilder.buildCommandReply(RequestAuthorizationReply, cmd, success, message);
    }
}
