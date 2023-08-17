import { Message } from "./Message";

/**
 * An event message.
 *
 * Events are simple notifications that do not require a reply nor will *execute* anything.
 */
export abstract class Event extends Message {
}
