import { v4 as uuidv4 } from "uuid";

import { UnitID } from "../../utils/UnitID";
import { MessageTypesCatalog } from "./MessageTypesCatalog";

export type MessageName = string;
export type Trace = string;

/**
 * Base class for all messages.
 *
 * A message, besides its actual data, consists mainly of information from where it came and where it should go.
 *
 * This class also offers a useful decorator to easily declare new messages, like in the following example:
 * ```
 *     @Message.define("msg/command")
 *     class MyCommand extends Command {
 *          ...
 *     }
 * ```
 */
export class Message {
    public name: MessageName = "";

    public origin: UnitID;
    public sender: UnitID;

    public target: Channel;

    public hops: UnitID[];

    public trace: Trace;

    public constructor(readonly origin: UnitID, readonly sender: UnitID, readonly target: Channel, readonly hops: UnitID[] = [],
                       readonly trace: Trace = uuidv4()) {
    }

    /**
     * Defines a new message.
     *
     * The decorator takes care of wrapping the new class as a dataclass, passing the correct message
     * name to its constructor. It also registers the new message type in the global ``MessageTypesCatalog``.
     *
     * Examples:
     * ```
     *     @Message.define("msg/command")
     *     class MyCommand extends Command {
     *         ...
     *     }
     * ```
     *
     * @param name - The name of the message.
     */
    public static define(name: string) {
        return (ctor: Function) => {
            let newClass = class extends ctor {
                public readonly name: MessageName = name;
            };

            MessageTypesCatalog.registerType(name, newClass.constructor);

            return newClass;
        }
    }
}

export interface MessageType {
    new(...args: any[]): object;
}
