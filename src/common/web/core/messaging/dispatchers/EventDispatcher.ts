import { Event } from "../Event";
import { MessageContext } from "../handlers/MessageContext";
import { MessageHandlerMapping } from "../handlers/MessageHandler";
import { EventMetaInformation } from "../meta/EventMetaInformation";
import { MessageDispatcher } from "./MessageDispatcher";

/**
 * Message dispatcher specific to ``Event``.
 */
export class EventDispatcher extends MessageDispatcher<Event, EventMetaInformation> {
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
    public dispatch<CtxType extends MessageContext>(msg: Event, msgMeta: EventMetaInformation, handler: MessageHandlerMapping, ctx: CtxType): void {
        ctx.logger.debug(`Dispatching event: ${String(msg)}`, "bus");
        super.dispatch(msg, msgMeta, handler, ctx);
    }
}
