import { Command } from "../../core/messaging/Command";
import { CommandReply } from "../../core/messaging/CommandReply";
import { CommandComposer } from "../../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../../core/messaging/composers/CommandReplyComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Message } from "../../core/messaging/Message";
import { AuthorizationTokenType } from "../../data/entities/authorization/AuthorizationToken";
import { type AuthorizationRequestPayload } from "../../integration/authorization/AuthorizationRequest";

/**
 * Command to perform an authorization request. Requires a ``RequestAuthorizationReply`` reply.
 */
@Message.define("command/authorization/request")
export class RequestAuthorizationCommand extends Command {
    public readonly payload: AuthorizationRequestPayload = {
        auth_id: "",
        auth_type: AuthorizationTokenType.Invalid,
        auth_issuer: "",
        auth_bearer: "",
        fingerprint: "",
    };
    public readonly strategy: string = "";
    public readonly data: any = null;

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        payload: AuthorizationRequestPayload,
        strategy: string,
        data: any,
        chain: Message | null = null,
    ): CommandComposer<RequestAuthorizationCommand> {
        return messageBuilder.buildCommand(
            RequestAuthorizationCommand,
            {
                payload: payload,
                strategy: strategy,
                data: data,
            },
            chain,
        );
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
