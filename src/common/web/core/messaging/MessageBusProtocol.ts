import { Message } from "./Message";
import { MessageMetaInformation } from "./meta/MessageMetaInformation";

/**
 * Defines the general interface for the ``MessageBus``.
 */
export interface MessageBusProtocol {
    dispatch(msg: Message, msgMeta: MessageMetaInformation): void;
}
