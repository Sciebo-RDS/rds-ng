import { Command } from "../../core/messaging/Command";
import { CommandReply } from "../../core/messaging/CommandReply";
import { CommandComposer } from "../../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../../core/messaging/composers/CommandReplyComposer";
import { MessageBuilder } from "../../core/messaging/composers/MessageBuilder";
import { Message } from "../../core/messaging/Message";
import { AuthorizationTokenType } from "../../data/entities/authorization/AuthorizationToken";
import { type UserID } from "../../data/entities/user/User";
import { type AuthorizationRequestPayload } from "../../integration/authorization/AuthorizationRequest";

/**
 * Command to perform an authorization request. Requires a ``RequestAuthorizationReply`` reply.
 *
 * @param payload - The authorization request information.
 * @param strategy - The token strategy (e.g., OAuth2).
 * @param data - The actual token request data.
 */
@Message.define("command/authorization/request")
export class RequestAuthorizationCommand extends Command {
    public readonly request_payload: AuthorizationRequestPayload = {
        auth_id: "",
        auth_type: AuthorizationTokenType.Invalid,
        auth_issuer: "",
        auth_bearer: "",
        fingerprint: ""
    };
    public readonly strategy: string = "";
    public readonly data: any = null;

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        request_payload: AuthorizationRequestPayload,
        strategy: string,
        data: any,
        chain: Message | null = null
    ): CommandComposer<RequestAuthorizationCommand> {
        return messageBuilder.buildCommand(
            RequestAuthorizationCommand,
            {
                request_payload: request_payload,
                strategy: strategy,
                data: data
            },
            chain
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
        message: string = ""
    ): CommandReplyComposer<RequestAuthorizationReply> {
        return messageBuilder.buildCommandReply(RequestAuthorizationReply, cmd, success, message);
    }
}

/**
 * Command to revoke an authorization. Requires a ``RevokeAuthorizationReply`` reply.
 *
 * @param user_id - The user ID.
 * @param auth_id - The ID of the token to revoke.
 * @param force - If true, the token will be removed immediately; otherwise, it will be marked as invalid only
 */
@Message.define("command/authorization/revoke")
export class RevokeAuthorizationCommand extends Command {
    public readonly user_id: UserID = "";
    public readonly auth_id: string = "";

    public readonly force: boolean = true;

    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        userID: UserID,
        authID: string,
        force: boolean = true,
        chain: Message | null = null
    ): CommandComposer<RevokeAuthorizationCommand> {
        return messageBuilder.buildCommand(RevokeAuthorizationCommand, { user_id: userID, auth_id: authID, force: force }, chain);
    }
}

/**
 * Reply to ``RevokeAuthorizationCommand``.
 */
@Message.define("command/authorization/revoke/reply")
export class RevokeAuthorizationReply extends CommandReply {
    /**
     * Helper function to easily build this message.
     */
    public static build(
        messageBuilder: MessageBuilder,
        cmd: RevokeAuthorizationCommand,
        success: boolean = true,
        message: string = ""
    ): CommandReplyComposer<RevokeAuthorizationReply> {
        return messageBuilder.buildCommandReply(RevokeAuthorizationReply, cmd, success, message);
    }
}
