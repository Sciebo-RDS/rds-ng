import { Event } from "../Event";
import { EventMetaInformation } from "../meta/EventMetaInformation";
import { MessageEntrypoint, MessageMetaInformation } from "../meta/MessageMetaInformation";
import { MessageComposer } from "./MessageComposer";

/**
 * Composer for ``Event`` messages.
 */
export class EventComposer<MsgType extends Event> extends MessageComposer<MsgType> {
    protected createMetaInformation(): MessageMetaInformation {
        return new EventMetaInformation(MessageEntrypoint.Local);
    }
}
