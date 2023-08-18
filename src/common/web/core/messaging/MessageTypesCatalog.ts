import { type Constructable } from "../../utils/Types";
import { type MessageName } from "./Message";

/**
 * Global catalog of all registered message types.
 *
 * This is a globally accessible list of all message types, associated with their respective message names.
 * It's mainly used to create proper message objects from incoming network messages.
 */
export class MessageTypesCatalog {
    private static _messageTypes: Record<MessageName, Constructable> = {};

    /**
     * Registers a new message type.
     *
     * @param name - The message name.
     * @param msgType - The message type.
     */
    public static registerType(name: MessageName, msgType: Constructable): void {
        if (name in this._messageTypes) {
            if (this._messageTypes[name] != msgType) {
                throw new Error(`A message with the name '${name}' has already been registered to a different message type`);
            }
        } else {
            this._messageTypes[name] = msgType;
        }
    }

    /**
     * Finds the message type associated with the given ``name``.
     *
     * @param name - The message name.
     *
     * @returns - The associated message type, if any.
     */
    public static findType(name: MessageName): Constructable | undefined {
        return name in this._messageTypes ? this._messageTypes[name] : undefined;
    }
}
