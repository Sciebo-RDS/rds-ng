import { wildcardMatch } from "wildcard-match";

import { type MessageHandler, MessageHandlerMapping, type MessageHandlerMappings } from "./MessageHandler";
import { Message, type MessageType } from "../Message";

/**
 * Holds mappings for message handlers.
 */
export class MessageHandlers {
    private readonly _mappings: MessageHandlerMappings = [];

    /**
     * Adds a new message handler mapping.
     *
     * @param filter - The message name filter.
     * @param handler - The message handler.
     * @param messageType - The message type the handler expects.
     */
    public addHandler(filter: string, handler: MessageHandler, messageType: MessageType = Message): void {
        this._mappings.push(new MessageHandlerMapping(filter, handler, messageType));
    }

    /**
     * Finds all handlers that fit the given ``msg_name``.
     *
     * The message name filter can be a complete message name, or a wildcard pattern using asterisks (*).
     *
     * @param msgName - The message name (pattern).
     *
     * @returns - A list of all found message handlers.
     */
    public findHandlers(msgName: string): MessageHandlerMappings {
        let matcher = wildcardMatch(msgName);
        let handlers: MessageHandlerMappings = [];
        for (const mapping of this._mappings) {
            if (matcher(mapping.filter)) {
                handlers.push(mapping);
            }
        }
        return handlers;
    }

    /**
     * Gets the string representation of all mapped handlers.
     */
    public toString(): string {
        return this._mappings.map((mapping) => mapping.toString()).join("; ");
    }
}
