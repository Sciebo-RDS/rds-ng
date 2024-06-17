// @ts-ignore
import { v4 as uuidv4 } from "uuid";
import { Message, type MessageCategory, type Trace } from "./Message";

/**
 * A command message.
 *
 * Commands are instructions that need to be *executed* by the receiving component.
 *
 * Notes:
 *     Commands need to *always* be replied by emitting a corresponding ``CommandReply``.
 *     This reply is then automatically sent back to the original sender.
 */
export class Command extends Message {
    public static readonly Category: MessageCategory = "Command";

    public readonly unique: Trace = uuidv4();

    /**
     * Gets the global message category.
     */
    public get messageCategory(): MessageCategory {
        return Command.Category;
    }
}
