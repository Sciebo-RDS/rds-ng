import { UnitID } from "../../utils/UnitID";
import { MessageTypesCatalog } from "./MessageTypesCatalog";
import { Channel } from "./Channel";
import { type Constructable } from "../../utils/Types";

// @ts-ignore
import { v4 as uuidv4 } from "uuid";

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
    /**
     * @param name - The name of the message.
     * @param origin - The initial source component of the message.
     * @param sender - The component from where the message came from.
     * @param target - Where the message should go to.
     * @param hops - A list of components the message was sent through.
     * @param trace - A unique trace identifying messages that logically belong together.
     */
    public constructor(readonly name: string, readonly origin: UnitID, readonly sender: UnitID, readonly target: Channel,
                       readonly hops: UnitID[] = [], readonly trace: Trace = uuidv4()) {
    }

    /**
     * Converts this message into its JSON representation.
     *
     * @returns - The JSON string representing this message.
     */
    public convertToJSON(): string {
        return JSON.stringify(this);
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
    public static define(name: string): Function {
        return (ctor: Constructable): Constructable => {
            let newClass = class extends ctor {
                public constructor(...args: any[]) {
                    super(name, ...args);
                }
            };

            MessageTypesCatalog.registerType(name, newClass);

            return newClass;
        }
    }
}

export type MessageType = Function;  // Class types are actually represented by their constructor function
