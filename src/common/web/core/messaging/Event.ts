import { Message, type MessageCategory } from "./Message";

/**
 * An event message.
 *
 * Events are simple notifications that do not require a reply nor will *execute* anything.
 */
export class Event extends Message {
    public static readonly Category: MessageCategory = "Event";

    /**
     * Gets the global message category.
     */
    public get messageCategory(): MessageCategory {
        return Event.Category;
    }
}
