import { MessageMetaInformationList } from "../meta/MessageMetaInformationList";
import { MessageMetaInformation } from "../meta/MessageMetaInformation";
import { Message } from "../Message";
import { MessageHandlerMapping } from "../handlers/MessageHandler";
import { MessageContext } from "../handlers/MessageContext";

/**
 * Base message dispatcher responsible for sending messages to registered handlers.
 *
 * Dispatching a message (locally) is done by passing the message to one or more registered message handlers within a ``Service``.
 * The message dispatcher also performs pre- and post-dispatching tasks and takes care of catching errors raised in a handler.
 */
export abstract class MessageDispatcher<MetaInfoType extends MessageMetaInformation> {
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
     *
     * @throws Error - If the meta information type is invalid.
     */
    public preDispatch<M extends Message>(msg: M, msgMeta: MetaInfoType): void {
        if (!(msgMeta instanceof T)) {
            throw new Error(`The meta information for dispatcher ${String(this)} is of the wrong type (${typeof msgMeta})`);
        }
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
    public dispatch<M extends Message, C extends MessageContext>(msg: M, msgMeta: MetaInfoType, handler: MessageHandlerMapping, ctx: C): void {
        if (msg instanceof handler.messageType) {
            try {
                ctx.begin(msgMeta.requiresReply);

                // The service context will not suppress errors so that the dispatcher can react to them
                handler.handler(msg, ctx);

                ctx.end();
            } catch (err) {
                ctx.reportError(e);
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
    public postDispatch<M extends Message>(msg: M, msgMeta: MetaInfoType): void {
    }

    protected contextError<M extends Message>(err: any, msg: M, msgMeta: MetaInfoType): void {
    }
}
