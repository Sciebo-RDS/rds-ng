import { Message, type MessageType } from "../Message";

export type MessageHandler = (msg: Message, ctx: Message) => void; // TODO! Ctx

/**
 * Mapping from a message name filter to a message handler.
 */
export class MessageHandlerMapping {
    /**
     * @param filter - The message name filter.
     * @param handler - The message handler.
     * @param messageType - The message type the handler expects.
     */
    public constructor(readonly filter: string, readonly handler: MessageHandler, readonly messageType: MessageType) {
    }

    /**
     * Gets the string representation of the handler mapping.
     */
    public toString(): string {
        return `${this.filter} -> ${String(this.handler)} [${String(this.messageType)}]`;
    }
}

export type MessageHandlerMappings = MessageHandlerMapping[];
