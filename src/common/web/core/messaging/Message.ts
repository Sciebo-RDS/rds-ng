import { plainToInstance, Type } from "class-transformer";
// @ts-ignore
import { v4 as uuidv4 } from "uuid";
import { Constructable } from "../../utils/Types";

import { UnitID } from "../../utils/UnitID";
import { Channel } from "./Channel";
import { MessageTypesCatalog } from "./MessageTypesCatalog";

export type MessageCategory = string;
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
export abstract class Message {
    public static readonly Category: MessageCategory = "Message";

    public readonly name: string;
    // @ts-ignore
    @Type(() => UnitID)
    public readonly origin: UnitID;
    // @ts-ignore
    @Type(() => UnitID)
    public readonly sender: UnitID;
    // @ts-ignore
    @Type(() => Channel)
    public readonly target: Channel;
    // @ts-ignore
    @Type(() => UnitID)
    public readonly hops: UnitID[];
    public readonly trace: Trace;

    /**
     * @param name - The name of the message.
     * @param origin - The initial source component of the message.
     * @param sender - The component from where the message came from.
     * @param target - Where the message should go to.
     * @param hops - A list of components the message was sent through.
     * @param trace - A unique trace identifying messages that logically belong together.
     */
    public constructor(name: string, origin: UnitID, sender: UnitID, target: Channel, hops: UnitID[] = [], trace: Trace = uuidv4()) {
        this.name = name;
        this.origin = origin;
        this.sender = sender;
        this.target = target;
        this.hops = hops;
        this.trace = trace;
    }

    /**
     * Converts this message to JSON.
     */
    public convertToJSON(): string {
        return JSON.stringify(this);
    }

    /**
     * Creates a message from JSON data.
     *
     * @param msgType - The message type to construct.
     * @param data - The JSON data string.
     *
     * @returns - The created message.
     */
    public static convertFromJSON(msgType: ConstructableMessage, data: string): Message {
        let objData = JSON.parse(data);
        return plainToInstance(msgType, objData) as Message;
    }

    /**
     * Retrieves the name of the message type on a message class basis.
     */
    public static messageName(): MessageName {
        return "";
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

                public static messageName(): MessageName {
                    return name;
                }
            };

            MessageTypesCatalog.registerItem(name, newClass);

            return newClass;
        };
    }

    /**
     * Gets the global message category.
     */
    public abstract get category(): MessageCategory;

    /**
     * Gets the string representation of this message.
     */
    public toString(): string {
        return this.convertToJSON();
    }
}

export interface ConstructableMessage<T extends Message = Message> {
    new(...args: any[]): T;

    messageName(): MessageName;
}
