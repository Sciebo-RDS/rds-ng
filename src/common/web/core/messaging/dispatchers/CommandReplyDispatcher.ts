import { CommandReply } from "../CommandReply";
import { MessageContext } from "../handlers/MessageContext";
import { MessageHandlerMapping } from "../handlers/MessageHandler";
import { CommandReplyMetaInformation } from "../meta/CommandReplyMetaInformation";
import { CommandDispatcher } from "./CommandDispatcher";
import { MessageDispatcher } from "./MessageDispatcher";

/**
 * Message dispatcher specific to ``CommandReply``.
 */
export class CommandReplyDispatcher extends MessageDispatcher<CommandReply, CommandReplyMetaInformation> {
    /**
     * Called to perform tasks *before* sending a message.
     *
     * This method is called before any service-registered message handler is invoked.
     *
     * @param msg - The message that is about to be dispatched.
     * @param msgMeta - The message meta information.
     *
     * @throws Error - If the meta information type is invalid.
     */
    public preDispatch<MsgType extends CommandReply>(msg: MsgType, msgMeta: CommandReplyMetaInformation): void {
        super.preDispatch(msg, msgMeta);

        CommandDispatcher.invokeReplyCallback(msg.unique, msg);
        MessageDispatcher._metaInformationList.remove(msg.unique);
    }

    /**
     * Dispatches a message to locally registered message handlers.
     *
     * Notes:
     *     Exceptions arising within a message handler will not interrupt the running program; instead, such errors will only be logged.
     *
     * @param msg - The message to be dispatched.
     * @param msgMeta - The message meta information.
     * @param handler - The handler to be invoked.
     * @param ctx - The message context.
     *
     * @throws Error - If the handler requires a different message type.
     */
    public dispatch<CtxType extends MessageContext>(msg: CommandReply, msgMeta: CommandReplyMetaInformation, handler: MessageHandlerMapping,
                                                    ctx: CtxType): void {
        ctx.logger.debug(`Dispatching command reply: ${String(msg)}`, "bus");
        super.dispatch(msg, msgMeta, handler, ctx);
    }
}
