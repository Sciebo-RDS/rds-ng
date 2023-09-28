import logging from "../../logging/Logging";
import { Event } from "../Event";
import { EventMetaInformation } from "../meta/EventMetaInformation";
import { MessageDispatcher } from "./MessageDispatcher";

/**
 * Message dispatcher specific to ``Event``.
 */
export class EventDispatcher extends MessageDispatcher<Event, EventMetaInformation> {
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
    public preDispatch<MsgType extends Event>(msg: MsgType, msgMeta: EventMetaInformation): void {
        logging.debug(`Dispatching event: ${String(msg)}`, "bus");
        super.preDispatch(msg, msgMeta);
    }
}
