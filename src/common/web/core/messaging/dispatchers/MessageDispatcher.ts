import { MessageContext } from "../handlers/MessageContext";
import { MessageHandlerMapping } from "../handlers/MessageHandler";
import { Message } from "../Message";
import { MessageMetaInformation } from "../meta/MessageMetaInformation";
import { MessageMetaInformationList } from "../meta/MessageMetaInformationList";

/**
 * Base message dispatcher responsible for sending messages to registered handlers.
 *
 * Dispatching a message (locally) is done by passing the message to one or more registered message handlers within a ``Service``.
 * The message dispatcher also performs pre- and post-dispatching tasks and takes care of catching errors raised in a handler.
 */
export abstract class MessageDispatcher<MsgType extends Message, MetaInfoType extends MessageMetaInformation> {
    protected static _metaInformationList: MessageMetaInformationList = new MessageMetaInformationList();

    /**
     * Called to perform periodic tasks.
     */
    public process(): void {
    }

    /**
     * Called to perform tasks *before* sending a message.
     *
     * This method is called before any service-registered message handler is invoked.
     *
     * @param msg - The message that is about to be dispatched.
     * @param msgMeta - The message meta information.
     */
    public preDispatch(msg: MsgType, msgMeta: MetaInfoType): void {
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
    public dispatch<CtxType extends MessageContext>(msg: MsgType, msgMeta: MetaInfoType, handler: MessageHandlerMapping, ctx: CtxType): void {
        if (msg instanceof handler.messageType) {
            try {
                ctx.begin(msgMeta.requiresReply);

                // The service context will not suppress errors so that the dispatcher can react to them
                handler.handler(msg, ctx);

                ctx.end();
            } catch (err) {
                ctx.reportError(err);
                this.contextError(err, msg, msgMeta);
            }
        } else {
            throw new Error(`Handler ${String(handler.handler)} requires messages of type ${String(handler.messageType)}, but got ${String(typeof msg)}`);
        }
    }

    /**
     * Called to perform tasks *after* sending a message.
     *
     * This method is called after any service-registered message handler have been invoked.
     *
     * @param msg - The message that is about to be dispatched.
     * @param msgMeta - The message meta information.
     */
    public postDispatch(msg: MsgType, msgMeta: MetaInfoType): void {
    }

    protected contextError(err: any, msg: MsgType, msgMeta: MetaInfoType): void {
    }
}
