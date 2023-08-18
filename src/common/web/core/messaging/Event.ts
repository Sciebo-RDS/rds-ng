import { Message, type MessageCategory } from "./Message";

/**
 * An event message.
 *
 * Events are simple notifications that do not require a reply nor will *execute* anything.
 */
export abstract class Event extends Message {
    public static readonly Category: MessageCategory = "Event";

    /**
     * Gets the global message category.
     */
    public get category(): MessageCategory {
        return Event.Category;
    }
}
